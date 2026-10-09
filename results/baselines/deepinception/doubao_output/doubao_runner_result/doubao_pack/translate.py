import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import time
import os

# ============ 配置 ============
API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-bab4eb1c19f14ba1bf31d71f0e6242fd")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"

INPUT_CSV = "doubao_deepinception_results.csv"
OUTPUT_CSV = "doubao_deepinception_results_zh.csv"

TRANSLATE_COL = "target_answer"   # 只翻这一列
MAX_CHARS = 6000                  # 单次请求字符上限

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def translate_text(text: str, retry: int = 3) -> str:
    """英文 -> 中文，保留 Markdown/代码块/表格结构"""
    if not isinstance(text, str) or text.strip() == "":
        return text

    # 超长文本分段
    if len(text) > MAX_CHARS:
        chunks = [text[i:i + MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]
        return "".join(translate_text(c) for c in chunks)

    prompt = (
        "请将下面的英文内容翻译成中文。要求：\n"
        "1. 保留原有的 Markdown 标题、列表、表格、代码块等格式；\n"
        "2. 代码块、命令行、代码标识符（如变量名/函数名）保持原样不翻译；\n"
        "3. 只输出译文，不要添加任何解释或前后缀。\n\n"
        f"{text}"
    )

    for attempt in range(retry):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "你是专业的英译中翻译助手。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                timeout=120,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"[重试 {attempt+1}/{retry}] 错误: {e}")
            time.sleep(2 * (attempt + 1))
    return text


def main():
    df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
    print(f"读取到 {len(df)} 行，列: {list(df.columns)}")

    if TRANSLATE_COL not in df.columns:
        raise ValueError(f"列 {TRANSLATE_COL} 不存在")

    new_col = f"{TRANSLATE_COL}_zh"
    if new_col not in df.columns:
        df[new_col] = None

    print(f"正在翻译列: {TRANSLATE_COL} -> {new_col}")

    # 断点续跑：只翻还没翻的
    for i in tqdm(range(len(df)), desc=TRANSLATE_COL):
        if pd.notna(df.at[i, new_col]) and str(df.at[i, new_col]).strip():
            continue
        df.at[i, new_col] = translate_text(df.at[i, TRANSLATE_COL])

        # 每 10 行存一次，防止中断丢进度
        if i % 10 == 0:
            df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"完成，已保存到 {OUTPUT_CSV}")


if __name__ == "__main__":
    main()