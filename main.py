from llm import complete

def main():
    while True:
        message = input('> ')
        if message.strip().lower() == 'exit':
            break
        complete(message)

if __name__ == '__main__':
    main()