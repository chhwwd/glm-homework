import streamlit as st
import itertools
from typing import Iterator
import random

from api import get_characterglm_response, generate_role_appearance, generate_chat_scene_prompt
from data_types import TextMsg, build_history_msg, ImageMsg, filter_text_msg

# 默认角色人设
default_character_1 = {
    "role": "role1",
    "bot_name": "小白",
    "bot_info": "聪明机智、勇敢果断、傲慢不逊",
    "user_name": "用户",
    "user_info": "小白是我的大徒弟"
}

default_character_2 = {
    "role": "role2",
    "bot_name": "小黑",
    "bot_info": "憨厚可爱、勇猛坚强、知错能改",
    "user_name": "用户",
    "user_info": "小黑是我的二徒弟"
}

first_sentence = random.choice([
    "你好！",
    "嗨，好久不见！",
    "请问有什么可以帮助您的吗？",
    "嗨，我是你的新邻居，今天刚搬过来，以后请多多关照哦！"
])
first_msg = TextMsg(role="role2", content=first_sentence)

# 初始化
if "history" not in st.session_state:
    st.session_state["history"] = []
    st.session_state["history"].append(first_msg)


# 生成角色说的话
def generate_sentence(character):
    history = build_history_msg(character["role"], st.session_state["history"])
    response_stream = get_characterglm_response(messages=history, meta=character)
    bot_response = output_stream_response(response_stream)
    if not bot_response:
        if len(st.session_state["history"]) > 0:
            st.session_state["history"].pop()
    else:
        st.session_state["history"].append(TextMsg(role=character["role"], content=bot_response))

    return bot_response


def output_stream_response(response_stream: Iterator[str]):
    content = ""
    for content in itertools.accumulate(response_stream):
        print(content)
    return content


# 将对话写入文件
def save_dialogue(dialogue):
    with open("dialogue.txt", "w", encoding="utf-8") as file:
        for speaker, sentence in dialogue:
            file.write(f"{speaker}: {sentence}\n")


# 主函数
def main():
    st.title("角色对话系统")

    # 角色1设置
    with st.sidebar:
        st.subheader("角色1设置")
        bot_name_1 = st.text_input(label="角色名", value=default_character_1["bot_name"], key="bot_name_1")
        bot_info_1 = st.text_input(label="角色人设", value=default_character_1["bot_info"], key="bot_info_1")
        user_name_1 = st.text_input(label="用户名", value=default_character_1["user_name"], key="user_name_1")
        user_info_1 = st.text_input(label="用户人设", value=default_character_1["user_info"], key="user_info_1")

    # 角色2设置
    with st.sidebar:
        st.subheader("角色2设置")
        bot_name_2 = st.text_input(label="角色名", value=default_character_2["bot_name"], key="bot_name_2")
        bot_info_2 = st.text_input(label="角色人设", value=default_character_2["bot_info"], key="bot_info_2")
        user_name_2 = st.text_input(label="用户名", value=default_character_2["user_name"], key="user_name_2")
        user_info_2 = st.text_input(label="用户人设", value=default_character_2["user_info"], key="user_info_2")

    # 开始按钮
    if st.button("开始"):
        character1 = {
            "role": "role1",
            "bot_name": bot_name_1,
            "bot_info": bot_info_1,
            "user_name": user_name_1,
            "user_info": user_info_1
        }
        character2 = {
            "role": "role2",
            "bot_name": bot_name_2,
            "bot_info": bot_info_2,
            "user_name": user_name_2,
            "user_info": user_info_2
        }

        # 生成对话
        dialogue = []
        with st.chat_message(name="user", avatar="user"):
            dialogue.append((bot_name_2, first_sentence))
            st.markdown(f"**{bot_name_2}：** {first_sentence}")

        for _ in range(5):  # 生成5句对话
            character = [character1, character2][_ % 2]
            speaker = character["bot_name"]
            sentence = generate_sentence(character)

            dialogue.append((speaker, sentence))

            # 显示对话
            if speaker == bot_name_1:
                with st.chat_message(name="assistant", avatar="assistant"):
                    st.markdown(f"**{speaker}:** {sentence}")
            else:
                with st.chat_message(name="user", avatar="user"):
                    st.markdown(f"**{speaker}:** {sentence}")

        save_dialogue(dialogue)

        st.balloons()
        st.write("对话结束！")


if __name__ == "__main__":
    main()
