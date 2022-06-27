def split_text_file(file_name, chunk_amount):
    with open(file_name, 'r') as initial_file:
        main = initial_file.readlines()
        divide = int(len(main) / chunk_amount)
    counter = 0
    while main:
        counter += 1
        file_initial_name = file_name.split('.')[0]
        with open(f'{file_initial_name}_chunk_{counter}.txt', 'w') as file:
            chunk = main[:divide]
            for line in chunk:
                file.writelines(str(line))
        for i in range(divide):
            main.remove(main[0])


split_text_file(input('file path> '), int(input('How many chunks> ')))
