import requests
import json
import re
from datetime import datetime

# Thay username của bạn vào đây
USERNAME = "ngxc.dev"

def get_tiktok_stats():
    url = f"https://www.tiktok.com/@{USERNAME}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        # TikTok thường để dữ liệu trong thẻ script hoặc meta
        # Đây là cách regex đơn giản để tìm follower count trong source HTML
        # Lưu ý: TikTok đổi cấu trúc HTML thường xuyên, regex này có thể cần cập nhật
        html = response.text

        # Tìm kiếm chuỗi kiểu "followerCount":1234 họăc trong meta tag
        # Pattern này chỉ là ví dụ, cần inspect element thực tế trên tiktok để tinh chỉnh
        match = re.search(r'"followerCount":(\d+)', html)

        if match:
            return match.group(1)
        else:
            # Fallback: Nếu không tìm thấy bằng regex, trả về None
            print("Could not find follower count in HTML")
            return None

    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    followers = get_tiktok_stats()

    if followers:
        print(f"Success! Followers: {followers}")

        # Đọc file cũ để giữ lại các data khác nếu có
        try:
            with open("stats.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Cập nhật số mới
        data["tiktok_followers"] = followers
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Lưu lại file
        with open("stats.json", "w") as f:
            json.dump(data, f, indent=2)
    else:
        print("Failed to fetch data. Keeping old data.")

if __name__ == "__main__":
    main()