import psutil

def get_installed_programs():
    installed_programs = {}

    # Проходим по всем процессам
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            # Получаем имя процесса и путь к исполняемому файлу
            process_name = proc.info['name']
            process_exe = proc.info['exe']

            # Добавляем в словарь только те программы, у которых есть имя и путь к исполняемому файлу
            if process_name and process_exe:
                installed_programs[process_name] = process_exe
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    return installed_programs

# Получаем и выводим список установленных программ
installed_programs = get_installed_programs()
res = []
for program, exe_path in installed_programs.items():
    program = program.lower()
    res.append(f"{program}, Path: {exe_path}")

res.sort()
for app in res: 
    print(app)
