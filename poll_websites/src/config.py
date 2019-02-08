from poll_websites.src.sendMessage import get_data_directory

html_dir = get_data_directory() + "html_elements/"
file_dir = get_data_directory() + "file_elements/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
receiver = "wernsdorfer@gmail.com"
