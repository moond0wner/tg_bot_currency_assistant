import aiohttp
from bs4 import BeautifulSoup


async def parse_course(url: str) -> dict:
    """Парсит сайт ЦБ РФ, получает курсы относительно рубля и возвращает результат в виде словаря"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                html_doc = await response.text()

        soup = BeautifulSoup(html_doc, "lxml")

        table = soup.find("table", {"class": "data"})
        courses = {}

        if table:
            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all("td")

                if cells and len(cells) >= 5:
                    code = cells[1].text.strip()
                    name = cells[3].text.strip()
                    course = cells[4].text.strip()
                    courses[code] = {name: course}
        return courses

    except (
        aiohttp.ClientError,
        Exception,
    ) as e:
        print(f"Error parsing course: {e}")


def format_courses_for_telegram(courses: dict) -> str:
    """Форматирует словарь для удобного чтения пользователем"""
    if not courses:
        return "Нет данных о курсах валют."

    formatted_lines = []
    for code, details in courses.items():
        for name, course in details.items():
            formatted_lines.append(
                f"{code}: {name}, {course}"
            )
    return "\n".join(sorted(formatted_lines))
