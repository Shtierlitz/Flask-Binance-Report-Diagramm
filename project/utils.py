

def read_file(file_path: str) -> dict[str, dict]:
    res = {}
    with open(file_path, 'r', encoding="UTF-8") as f:

        for i, line in enumerate(f.read().split(' ')[1:]):
            res.update({i:[line]})
        print(res)

read_file("./data/BTCUSDT_4h.csv")
