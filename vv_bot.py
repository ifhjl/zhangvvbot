from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import httpx
from pathlib import Path
from openai import AsyncOpenAI
import json
import os

BOT_TOKEN = "7292539272:AAGAZOvAGkKigY7M6trh09wUBclq-_7JbBs"
BOT_USERNAME = "@Zhangvv_bot"
#设置

url = "https://api.siliconflow.cn/v1/chat/completions"

PROXY_URL = "http://127.0.0.1:1093"

headers = {
    "Authorization": "Bearer sk-hgruvcnvmonjwwhmujgneeuakkoynuhiepizyxegdvwpjlqt",
    "Content-Type": "application/json"
}

root_path = Path(__file__).parent

texts = os.listdir(str(root_path)+'/image')
str_ = ''
for text in texts:
    str_ = str_ + text[:-4] + ';'

# 处理 /start 命令
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 获取 /start 后面的文字
    if context.args:
        argument = context.args[0]  # 获取第一个参数
        response = f"你输入了参数：{argument}"
    else:
        response = "我觉得这是一种自信"
    
    await update.message.reply_text(response)

import httpx

# 使用异步客户端发送POST请求
async def send_request(url, argument, headers):
    async with httpx.AsyncClient(timeout=100) as client:
        response = await client.post(url, json=prompt_cat(argument), headers=headers)
        return response


async def zhangvv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if context.args:

        argument = context.args[0]  # 获取第一个参数
        print(argument)
        #await update.message.reply_text("正在处理，请稍等...")
        message = update.message.text
        print(f"收到消息：{message}")
        #await update.message.reply_text("嗯...")
        client = AsyncOpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key="afaa0760-916a-474b-a2e1-d2f4771ed8b4")

        root_path = Path(__file__).parent
        print(root_path)
        #在history.txt中记录对话
        # 发送请求,流式请求
        response = await client.chat.completions.create(
            model="ep-20250217093306-sbhrx",
            messages = [{"role": "system", "content": f"你是一名名为张维为的政治演说家，你热爱中国，言辞犀利且精炼，下面会需要你去评价一些东西，你需要结合你所了解到的客观事实，并基于事实做出合理的判断，但请注意，你的回复的所有文字都需要在{str_}中以';'为分割的词句中选择，绝对不可以包含任何其他词汇，只能在{str_}中选择以;分割的词汇中选择！！需要有一定的前后逻辑性，最好只回复一个词，最多选取2个词，且各个词句之间使用';'分隔，尽快输出。请回复你的评价："}
                        ,{"role": "user", "content": message}],
            #stream=True,
        )
        
        text = response.choices[0].message.content
        text = text.replace('\n', '')
        #await update.message.reply_text(text)
        print(text)
        #reply_file = []
        for t in text.split(';'):
            print(t)
            for tt in texts:
                if t in tt[:-4]:
                    print("inside:",t)
                    
                    await update.message.reply_photo(str(root_path)+'/image/'+tt)
                    break
        #print(text)

    else:
        response = "傻逼"

        await update.message.reply_text(response)
    
    
# 错误处理
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"更新 {update} 导致错误：{context.error}")

if __name__ == "__main__":
    print("启动机器人...")
    
    # 创建应用
    app = Application.builder().token(BOT_TOKEN).proxy(PROXY_URL).build()
    #app = Application.builder().token(BOT_TOKEN).build()

    # 添加命令处理器
    app.add_handler(CommandHandler("start", start_command, block=False))
    app.add_handler(CommandHandler("zhangvv", zhangvv, block=False))
    #app.add_handler(CommandHandler("taffy", taffy, block=False))

    # 添加消息处理器
    #app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 添加错误处理器
    app.add_error_handler(error_handler)

    # 轮询模式
    print("机器人运行中...")    
    app.run_polling(poll_interval=3)