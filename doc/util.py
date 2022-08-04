def gen_packages_md():
    lines = []
    color = ['red', 'green', 'blue']
    with open("packages.txt", "r", encoding="UTF-16LE") as f:
        n = 0
        while f.readable():
            package = f.readline()
            if package == "":
                break
            package = package.split('==')
            sp = package[0].split("\ufeff")
            package[0] = sp[1] if len(sp) > 1 else sp[0]
            package[0] = package[0].replace('-', '_')
            package[1] = package[1].split('\n')[0]
            lines.append(f'![{package[0]} : {package[1]}](https://img.shields.io/badge/{package[0]}-{package[1]}-{color[n % len(color)]})\n')
            n += 1

    with open("packages.md", "w") as f:
        for line in lines:
            f.write(line)
