import asyncio
import re
from flask import Flask, request, jsonify
from playwright.async_api import async_playwright

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    urls_input = request.form.get("url")
    email_input = request.form.get("email", "").strip()  # Get email parameter, default to empty string
    phone_input = request.form.get("phone", "").strip()  # Get phone parameter, default to empty string

    if not urls_input:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    urls = [url.strip() for url in urls_input.split(",") if url.strip()]
    print(f"Received URLs: {urls}")
    print(f"Received Email: {email_input}")
    print(f"Received Phone: {phone_input}")
    
    if not urls:
        return jsonify({"error": "No valid URLs provided"}), 400

    result = asyncio.run(scrape_multiple_websites(urls, email_input, phone_input))
    print(f"Scraping result: {result}")
    return jsonify(result)


async def scrape_multiple_websites(initial_urls, input_email="", input_phone=""):
    visited = set()
    final_result = {
        "website": "-",
        "facebook": "-",
        "instagram": "-",
        "linkedin": "-",
        "google_maps": "-",
        "email": "-",
        "phone": "-"
    }
    
    # Track what information we already have from input
    input_provided = {
        "website": False,
        "facebook": False,
        "instagram": False,
        "linkedin": False,
        "google_maps": False,
        "email": False,
        "phone": False
    }

    # If email is provided in input, use it immediately
    if input_email and input_email != "-":
        final_result["email"] = input_email
        input_provided["email"] = True

    # If phone is provided in input, use it immediately
    if input_phone and input_phone != "-":
        final_result["phone"] = input_phone
        input_provided["phone"] = True

    # First, extract information directly from input URLs
    for url in initial_urls:
        input_data = extract_links_from_input(url)
        for key in final_result:
            if final_result[key] == "-" and input_data.get(key) and input_data[key] != "-":
                final_result[key] = input_data[key]
                input_provided[key] = True  # Mark as provided by input

    async def recursive_scrape(urls):
        new_urls = []

        for url in urls:
            normalized = normalize_url(url)
            if normalized in visited:
                continue
            visited.add(normalized)

            # Determine content type based on URL
            content_type = get_content_type(url)
            print(f"Visiting: {url} (content_type: {content_type})")

            result = await scrape_website(url, content_type)
            extracted_links = extract_links(result)

            # Update final result ONLY for information NOT provided in input
            for key in final_result:
                if (final_result[key] == "-" and 
                    not input_provided[key] and  # Only if not provided in input
                    extracted_links.get(key) and 
                    extracted_links[key] != "-"):
                    final_result[key] = extracted_links[key]
                    if key != "phone" and key != "email":  # Don't crawl phone numbers or emails
                        new_urls.append(extracted_links[key])  # To crawl deeper

    # Start recursive crawl only for missing information that wasn't provided in input
    urls_to_scrape = []
    for url in initial_urls:
        # Only scrape URLs that are not already providing the specific information we need
        url_type = get_url_type(url)
        if url_type == "website" or not input_provided.get(url_type, False):
            urls_to_scrape.append(url)
    
    if urls_to_scrape:
        await recursive_scrape(urls_to_scrape)
    
    return final_result


def get_url_type(url):
    """Determine what type of information this URL provides"""
    url_lower = url.lower()
    if "facebook.com" in url_lower:
        return "facebook"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "linkedin.com" in url_lower:
        return "linkedin"
    elif ("maps.google.com" in url_lower or 
          "goo.gl/maps" in url_lower or 
          "google.com/maps" in url_lower):
        return "google_maps"
    elif "@" in url:
        return "email"
    else:
        return "website"


def normalize_url(url):
    return url.lower().strip().rstrip("/")


def format_phone_number(phone):
    """
    Clean and format phone number by removing all spacing, brackets, and hyphens
    """
    if not phone or phone == "-":
        return phone
    
    # Remove all non-digit characters except the leading plus sign
    if phone.startswith('+'):
        # Keep the plus sign and remove everything else except digits
        formatted = '+' + re.sub(r'[^\d]', '', phone[1:])
    else:
        # Remove all non-digit characters
        formatted = re.sub(r'[^\d]', '', phone)
    
    return formatted


def extract_phone_numbers(text):
    """
    Extract phone numbers from text while filtering out HTML/CSS numeric values
    """
    # Remove HTML tags and CSS content to get clean text
    clean_text = remove_html_and_css_content(text)
    
    # Phone number patterns with context awareness
    phone_patterns = [
        # Pattern with phone-related keywords nearby
        r'(?i)(?:phone|tel|call|mobile|cell|contact|number)[\s:]*([+]?[\d\s\-\(\)\.]{7,18})',
        
        # Pattern with tel: or phone: prefix
        r'(?i)(?:tel:|phone:|call:)\s*([+]?[\d\s\-\(\)\.]{7,18})',
        
        # Pattern with specific formatting (parentheses, dashes, dots)
        r'\b([+]?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})\b',
        
        # International format with country code
        r'\b([+][1-9]\d{0,3}[-.\s]?\(?[0-9]{2,4}\)?[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4})\b',
        
        # Phone numbers in structured contact sections
        r'(?i)(?:contact|phone|tel|mobile|call)[\s\S]{0,50}?([+]?[\d\s\-\(\)\.]{10,18})',
    ]
    
    found_phones = set()
    
    for pattern in phone_patterns:
        matches = re.finditer(pattern, clean_text)
        for match in matches:
            phone_candidate = match.group(1) if match.groups() else match.group(0)
            
            # Clean and validate the phone number
            cleaned_phone = clean_phone_number(phone_candidate)
            
            if is_valid_phone_number(cleaned_phone, clean_text, match.start()):
                # Format the phone number by removing all spacing, brackets, and hyphens
                formatted_phone = format_phone_number(cleaned_phone)
                found_phones.add(formatted_phone)
    
    return list(found_phones)


def remove_html_and_css_content(text):
    """
    Remove HTML tags, CSS, JavaScript, and other non-content elements
    """
    # Remove script and style tags with their content
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    # Remove CSS rules (anything between curly braces that looks like CSS)
    text = re.sub(r'\{[^}]*\}', '', text)
    
    # Remove HTML attributes that might contain numeric values
    text = re.sub(r'(?i)(?:width|height|top|left|right|bottom|margin|padding|font-size|line-height)[\s]*:[\s]*[\d\.\s]+(?:px|em|rem|%|pt)?', '', text)
    
    # Remove HTML tags but keep the content
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Remove common CSS/HTML numeric patterns
    text = re.sub(r'\b(?:px|em|rem|pt|%|vh|vw|deg)\b', '', text)
    
    # Remove hex colors and other CSS values
    text = re.sub(r'#[0-9a-fA-F]{3,6}\b', '', text)
    text = re.sub(r'rgb\([^)]+\)', '', text)
    text = re.sub(r'rgba\([^)]+\)', '', text)
    
    # Remove data attributes and IDs that might contain numbers
    text = re.sub(r'(?i)(?:id|class|data-[\w-]+)[\s]*=[\s]*["\'][^"\']*["\']', '', text)
    
    # Remove URLs
    text = re.sub(r'https?://[^\s<>"\']+', '', text)
    
    # Remove email addresses (to avoid confusion with phone numbers)
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def is_valid_phone_number(phone, context_text, position):
    """
    Validate if the extracted phone number is actually a phone number
    """
    # Remove all non-digit characters to count digits
    digits_only = re.sub(r'[^\d]', '', phone)
    
    # Basic length check (7-15 digits is typical for phone numbers)
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False
    
    # Check if it's too short for a real phone number
    if len(digits_only) < 10 and not phone.startswith('+'):
        return False
    
    # Reject if all digits are the same
    if len(set(digits_only)) <= 1:
        return False
    
    # Reject sequential numbers (like 1234567890)
    if is_sequential_number(digits_only):
        return False
    
    # Check context around the phone number for validation
    if not has_phone_context(context_text, position):
        # If no phone context, apply stricter validation
        if len(digits_only) < 10:
            return False
        
        # Check if it looks like a timestamp, ID, or other non-phone number
        if is_likely_non_phone_number(phone, digits_only):
            return False
    
    # Reject if it looks like a CSS/HTML measurement
    if is_css_measurement(phone):
        return False
    
    # Reject if it's part of a URL, email, or file path
    if is_part_of_url_or_path(phone):
        return False
    
    return True


def is_sequential_number(digits):
    """Check if digits form a sequential pattern"""
    if len(digits) < 4:
        return False
    
    # Check for ascending sequence
    ascending = all(int(digits[i]) == int(digits[i-1]) + 1 for i in range(1, min(len(digits), 6)))
    
    # Check for descending sequence
    descending = all(int(digits[i]) == int(digits[i-1]) - 1 for i in range(1, min(len(digits), 6)))
    
    return ascending or descending


def has_phone_context(text, position):
    """
    Check if the phone number appears in a phone-related context
    """
    # Extract surrounding text (100 characters before and after)
    start = max(0, position - 100)
    end = min(len(text), position + 100)
    surrounding_text = text[start:end].lower()
    
    # Phone-related keywords
    phone_keywords = [
        'phone', 'tel', 'call', 'mobile', 'cell', 'contact', 'number',
        'telephone', 'fax', 'hotline', 'helpline', 'support', 'customer service',
        'office', 'business', 'emergency', 'dial', 'reach us', 'get in touch'
    ]
    
    return any(keyword in surrounding_text for keyword in phone_keywords)


def is_likely_non_phone_number(phone, digits_only):
    """
    Check if the number is likely not a phone number based on patterns
    """
    # Check for timestamp-like patterns (Unix timestamps, dates)
    if len(digits_only) >= 10 and digits_only.startswith(('19', '20', '16', '15')):
        return True
    
    # Check for ID-like patterns (very large numbers)
    if len(digits_only) > 12:
        return True
    
    # Check for version numbers or technical identifiers
    if re.match(r'^\d+\.\d+\.\d+', phone):
        return True
    
    return False


def is_css_measurement(phone):
    """Check if the number looks like a CSS measurement"""
    css_pattern = r'^\d+(?:\.\d+)?(?:px|em|rem|pt|%|vh|vw|deg)?$'
    return re.match(css_pattern, phone.strip())


def is_part_of_url_or_path(phone):
    """Check if the number is part of a URL or file path"""
    # Check for URL-like patterns
    if '/' in phone or '\\' in phone or '.' in phone and len(phone.split('.')) > 2:
        return True
    
    return False


def extract_links(scraped_data):
    """Extract links and phone numbers from scraped data"""
    data = {
        "website": "-",
        "facebook": "-",
        "instagram": "-",
        "linkedin": "-",
        "google_maps": "-",
        "email": "-",
        "phone": "-"
    }

    # Extract URLs with improved patterns
    patterns = {
        "website": r"https?://(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}(?:/[^\s\"'<>\[\]{}|\\^`]*)?",
        "facebook": r"https?://(?:www\.)?facebook\.com/[a-zA-Z0-9._-]+/?(?:\?[^\s\"'<>]*)?",
        "instagram": r"https?://(?:www\.)?instagram\.com/[a-zA-Z0-9._-]+/?(?:\?[^\s\"'<>]*)?",
        "linkedin": r"https?://(?:www\.)?linkedin\.com/(?:in/|company/)[a-zA-Z0-9._-]+/?(?:\?[^\s\"'<>]*)?",
        "google_maps": r"https?://(?:www\.)?(?:maps\.google\.com/|goo\.gl/maps/)[^\s\"'<>\[\]{}|\\^`]+",
        "email": r"\b[a-zA-Z0-9](?:[a-zA-Z0-9._-]*[a-zA-Z0-9])?@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b",
    }

    # Extract phone numbers using improved method
    phone_numbers = extract_phone_numbers(scraped_data)
    if phone_numbers:
        data["phone"] = phone_numbers[0]  # Take the first valid phone number (already formatted)

    # Extract other data
    for key, pattern in patterns.items():
        matches = re.findall(pattern, scraped_data, re.IGNORECASE)
        if matches:
            # Take the first valid match
            for match in matches:
                if isinstance(match, tuple):
                    url = ''.join(match)
                else:
                    url = match
                
                # Clean up the URL
                if key != "email" and not url.startswith('http'):
                    url = 'https://' + url
                
                # Validate the URL format
                if is_valid_url(url, key):
                    data[key] = url
                    break

    return data


def clean_phone_number(phone):
    """Clean and format phone number"""
    # Remove common prefixes and extra text
    phone = re.sub(r'(?:tel:|phone:|call:|mobile:|cell:)', '', phone, flags=re.IGNORECASE)
    
    # Keep only digits, spaces, hyphens, dots, parentheses, and plus sign
    phone = re.sub(r'[^\d\s\-\.\(\)\+]', '', phone).strip()
    
    # Remove extra spaces
    phone = re.sub(r'\s+', ' ', phone)
    
    return phone


def is_valid_phone(phone):
    """Validate if the extracted phone number is valid (legacy function for compatibility)"""
    digits_only = re.sub(r'[^\d]', '', phone)
    
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False
    
    if len(set(digits_only)) <= 2:
        return False
    
    is_sequential = all(int(digits_only[i]) == int(digits_only[i-1]) + 1 for i in range(1, min(len(digits_only), 5)))
    if is_sequential:
        return False
    
    return True


def is_valid_url(url, url_type):
    """Validate if the extracted URL is valid for the given type"""
    url_lower = url.lower()
    
    # Common invalid patterns to reject
    invalid_patterns = [
        r'\.(?:png|jpg|jpeg|gif|css|js|ico|svg|woff|ttf|eot)(?:\?|$)',  # File extensions
        r'data:',  # Data URLs
        r'javascript:',  # JavaScript URLs
        r'mailto:',  # Mailto links
        r'[{}|\[\]\\^`]',  # Invalid URL characters
        r'@\d+x\.', # Sprite/image references like @2x.
        r'sprite-', # Sprite references
        r'ui@\d+\.\d+', # UI version references
    ]
    
    # Check for invalid patterns
    for pattern in invalid_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return False
    
    if url_type == "facebook":
        return "facebook.com" in url_lower and url.startswith("http")
    elif url_type == "instagram":
        return "instagram.com" in url_lower and url.startswith("http")
    elif url_type == "linkedin":
        return "linkedin.com" in url_lower and url.startswith("http")
    elif url_type == "google_maps":
        return (("maps.google.com" in url_lower or 
                "goo.gl/maps" in url_lower or 
                "google.com/maps" in url_lower) and url.startswith("http"))
    elif url_type == "email":
        # More strict email validation
        email_pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9._-]*[a-zA-Z0-9])?@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, url) is not None
    elif url_type == "website":
        # More strict website validation
        return (url.startswith("http") and 
                "." in url and 
                not any(invalid in url_lower for invalid in ['data:', 'javascript:', 'mailto:']) and
                re.match(r'https?://(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}', url))
    
    return False


def get_content_type(url):
    """Determine content type based on URL"""
    url_lower = url.lower()
    if "facebook.com" in url_lower or "linkedin.com" in url_lower:
        return "text"
    elif "instagram.com" in url_lower:
        return "html"  # Changed from "text" to "html" for Instagram
    elif ("maps.google.com" in url_lower or 
          "goo.gl/maps" in url_lower or 
          "google.com/maps" in url_lower):
        return "maps"
    else:
        return "html"


def extract_links_from_input(url):
    """Extract information directly from the input URL"""
    data = {
        "website": "-",
        "facebook": "-",
        "instagram": "-",
        "linkedin": "-",
        "google_maps": "-",
        "email": "-",
        "phone": "-"
    }

    url_lower = url.lower()
    
    # Check if the URL itself contains the information we need
    if "facebook.com" in url_lower:
        data["facebook"] = url
    elif "instagram.com" in url_lower:
        data["instagram"] = url
    elif "linkedin.com" in url_lower:
        data["linkedin"] = url
    elif ("maps.google.com" in url_lower or 
          "goo.gl/maps" in url_lower or 
          "google.com/maps" in url_lower):
        data["google_maps"] = url
    elif "@" in url:  # If it's an email
        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", url)
        if email_match:
            data["email"] = email_match.group(0)
    else:
        # If it's a regular website URL
        data["website"] = url

    return data

async def wait_for_page_load(page, content_type):
    """Dynamic waiting strategy based on content type and page load indicators"""
    
    if content_type == "maps":
        # For Google Maps, wait for specific map elements to load
        try:
            await page.wait_for_selector('[data-value="Directions"]', timeout=15000)
        except:
            try:
                await page.wait_for_selector('[role="main"]', timeout=10000)
            except:
                await page.wait_for_load_state('networkidle', timeout=20000)
    
    elif content_type == "text":
        # For social media sites (Facebook, LinkedIn), wait for main content areas
        if "facebook.com" in page.url.lower():
            try:
                await page.wait_for_selector('[role="main"], [data-pagelet="root"]', timeout=15000)
            except:
                await page.wait_for_load_state('networkidle', timeout=10000)
        
        elif "linkedin.com" in page.url.lower():
            try:
                await page.wait_for_selector('main, [data-test-id], .profile-rail-card', timeout=15000)
            except:
                await page.wait_for_load_state('networkidle', timeout=10000)
        
        else:
            # Generic social media wait
            await page.wait_for_load_state('networkidle', timeout=10000)
    
    else:
        # For regular websites and Instagram (now treated as HTML)
        try:
            # Wait for network to be idle (no requests for 500ms)
            await page.wait_for_load_state('networkidle', timeout=15000)
        except:
            try:
                # Fallback: wait for DOMContentLoaded + additional time for dynamic content
                await page.wait_for_load_state('domcontentloaded', timeout=10000)
                # Check if page is still loading by monitoring changes
                await wait_for_content_stability(page)
            except:
                # Final fallback: basic wait
                await asyncio.sleep(3)

async def wait_for_content_stability(page, max_checks=10, stability_time=2):
    """Wait for page content to stabilize (stop changing)"""
    previous_content_length = 0
    stable_count = 0
    
    for _ in range(max_checks):
        try:
            current_content_length = await page.evaluate('document.body.innerHTML.length')
            
            if current_content_length == previous_content_length:
                stable_count += 1
                if stable_count >= stability_time:  # Content stable for 2 checks
                    break
            else:
                stable_count = 0
                previous_content_length = current_content_length
            
            await asyncio.sleep(1)
        except:
            await asyncio.sleep(1)

async def scrape_website(url, content_type):
    """
    Scrape website content using Playwright with dynamic waiting
    """
    try:
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = await context.new_page()
            
            # Navigate to the URL with timeout
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Dynamic waiting based on content type
            await wait_for_page_load(page, content_type)
            
            if content_type == "text":
                # For Facebook and LinkedIn, extract text content
                content = await page.evaluate("""
                    () => {
                        // Remove script and style elements
                        const scripts = document.querySelectorAll('script, style');
                        scripts.forEach(el => el.remove());
                        
                        // Get text content
                        return document.body.innerText || document.body.textContent || '';
                    }
                """)
            elif content_type == "maps":
                # For Google Maps, extract both HTML and text content
                content = await page.evaluate("""
                    () => {
                        // Get both HTML content and text content for Google Maps
                        const htmlContent = document.documentElement.outerHTML;
                        
                        // Also get text content
                        const scripts = document.querySelectorAll('script, style');
                        scripts.forEach(el => el.remove());
                        const textContent = document.body.innerText || document.body.textContent || '';
                        
                        return htmlContent + '\\n\\n' + textContent;
                    }
                """)
            else:
                # For regular websites and Instagram, get HTML content
                content = await page.content()

            # append content to a file
            # with open("scraped.txt", "a", encoding="utf-8") as file:
            #     file.write(f"URL: {url}\n")
            #     file.write(content + "\n\n")
            
            # Close browser
            await browser.close()
            
            return content
            
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
