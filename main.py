from collections import defaultdict
from demotivator import DemotivatorMaker
import random
import re

class MarkovChain:
    def __init__(self, order: int = 2):
        self.order = order          #кол-во слов в контексте
        self.chain = defaultdict(list)

    def train(self, tokens: list) -> None:
        if len(tokens) <= self.order:
            raise ValueError("Текст слишком короткий для обучения цепи Маркова.")
        
        for i in range(len(tokens) - self.order):
            key = tuple(tokens[i:i + self.order])
            next_word = tokens[i + self.order]
            self.chain[key].append(next_word)

    def generate(self, length: int = 50, seed: tuple = None) -> str:
        if not self.chain:
            return ""

        if seed and seed in self.chain:
            current_key = seed
        else:
            current_key = random.choice(list(self.chain.keys()))

        result = list(current_key)

        for _ in range(length):
            if current_key not in self.chain:
                break  
            next_word = random.choice(self.chain[current_key])
            result.append(next_word)
            current_key = tuple(result[-self.order:])

        return " ".join(result)
    
def main():
    print("Загрузка текста...")

    raw_text = open('data/sample.txt', 'r', encoding='utf-8').read()
    
    print("Токенизация...")

    tokens = []
    for word in raw_text.split():
        clean = re.sub(r"^[^\w]+|[^\w]+$", "", word).lower()
        if clean:
            tokens.append(clean)

    print(f"Найдено токенов: {len(tokens)}")

    print("Создание цепей Маркова...")
    model = MarkovChain(order=3)
    model.train(tokens)

    print("Генерация...")
    generated_text = model.generate(length=50)
    
    print("\n" + "="*60)
    print(generated_text.capitalize() + ".")
    print("="*60)

    demotivator_text = model.generate(length=random.randint(1,5))

    images = ["data/img1.jpg", "data/img2.jpg", "data/img3.jpg"]
    chosen_img = random.choice(images)

    maker = DemotivatorMaker()
    maker.make(chosen_img, demotivator_text, "output/demotivator.jpg")

if __name__ == "__main__":
    main()