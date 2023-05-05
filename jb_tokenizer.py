import logging
import re
import string
import jsonlines

import jieba
import jieba.posseg as pseg

jieba.setLogLevel(logging.ERROR)
jieba.set_dictionary("dict/dict.txt.big")
jieba.load_userdict("dict/user.txt")


def tokenize_one_jsonl(pub_file):
    with jsonlines.open(pub_file) as publications:
        for p in publications:
            text_tokens = tokenize(p["text"])
            title_tokens = tokenize(p["title"])
            comments_tokens = [
                {**c, "text": tokenize(c["text"])} for c in p["comments"]
            ]

            yield {
                "id": p["id"],
                "producer_id": p["producer_id"],
                "version": p["version"],
                "title": title_tokens,
                "text": text_tokens,
                "comments": comments_tokens,
            }


def remove_non_words(text):
    chinese_punctuations = (
        "※！？｡。＂＃＄％＆＇《》（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〿–—‘’‛“”„‟…‧﹏."
    )
    token_to_remove = string.punctuation + string.digits + chinese_punctuations
    text = text.translate(str.maketrans("", "", token_to_remove))
    text = re.sub(r"[\n\s\t]", "", text)
    return text


def tokenize(text):
    text = remove_non_words(text)
    tokens = [item.word for item in pseg.lcut(text)]
    return tokens
