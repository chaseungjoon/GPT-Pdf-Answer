from PyPDF2 import PdfReader
import openai
import os

def chat_completion(param, model):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'system', 'content': ''},
            {'role': 'user', 'content': 'Answer the numbered questions in the following text : ' + param}
        ],
        temperature=0.2
    )
    return response['choices'][0]['message']['content']


def save_file_list(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name[-4:] == '.pdf':
                file_list.append(root+'/'+file_name)
    return file_list

#Select GPT Model
while True:
    GPT_model = input("Select a GPT Model\n• gpt-3.5-turbo : Fast, Moderate Quality results\n• gpt-4 : Slow, Great Quality results\n>> ").strip()
    if GPT_model != 'gpt-3.5-turbo' and GPT_model != 'gpt-4':
        print("Type the name of the model correctly\n")
    else:
        break

# Input folder directory
folder_path = input("Enter folder directory for PDFs >> ").strip()
f_list = save_file_list(folder_path)
print(f'Total of {len(f_list)} PDFs')

for i in range(len(f_list)):
    # Initialize answer array
    ans = []

    # Fetch file directory from file list array
    f_dir = f_list[i]

    # Set output location, name
    output = folder_path + '/' + os.path.splitext(os.path.basename(f_dir))[0] +'_GPTAnswer' + ".txt"

    # Read PDF and save answer
    with open(f_dir, "rb") as f:
        pdf_reader = PdfReader(f)
        p_cnt = 1
        for page in pdf_reader.pages:
            print(f'PDF #{i+1} Solving...Page({p_cnt}/{len(pdf_reader.pages)})')
            ans.append(chat_completion(page.extract_text(),GPT_model))
            p_cnt += 1

    # Write answer to txt file
    with open(output, "w", encoding='utf-8') as file:
        for text in ans:
            try:
                file.write(text+"\n")
            except UnicodeEncodeError:
                continue

    print(f'PDF #{i+1} Complete!')