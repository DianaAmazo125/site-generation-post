from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    post_text = ""
    error_message = ""
    
    # Извлекаем данные из прошлых вводов, чтобы форма не сбрасывалась
    product_name = ""
    product_desc = ""
    product_price = ""
    selected_mood = "expert"

    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        product_desc = request.form.get('product_desc', '').strip()
        product_price = request.form.get('product_price', '').strip()
        selected_mood = request.form.get('mood', 'expert')

        # Жесткая проверка ТЗ: описание обязательно!
        if not product_desc:
            error_message = "⚠️ Пожалуйста, заполните обязательное поле с описанием товара!"
        else:
            name_part = f"«{product_name}»" if product_name else "Наш новый продукт"
            price_part = f"всего за {product_price}" if product_price else "по супер-выгодной цене"

            # Логика текстовых шаблонов в зависимости от настроения
            if selected_mood == 'expert':
                post_text = (
                    f"🎯 Представляем профессиональное решение: {name_part}.\n\n"
                    f"Данный продукт разработан специально для эффективного решения ваших задач. "
                    f"Ключевая особенность: {product_desc}. Каждая деталь спроектирована "
                    f"с упором на надежность и долгосрочный результат.\n\n"
                    f"💳 Инвестируйте в качество {price_part}. Оформить заказ можно прямо сейчас!"
                )
            elif selected_mood == 'friendly':
                post_text = (
                    f"✨ Приветик! Смотри, какую крутую штуку мы для тебя нашли — {name_part}! 🥰\n\n"
                    f"Если ты давно искал решение, то это именно оно. Посуди сам: {product_desc}. "
                    f"Мы сами в полном восторге и уверены, что тебе точно зайдет эта новинка!\n\n"
                    f"🎁 Забирай свой экземпляр {price_part}. Напиши нам в директ, обо всем расскажем! 💌"
                )
            elif selected_mood == 'funny':
                post_text = (
                    f"🚀 Внимание, шок-контент! {name_part} врывается в этот чат! 🤪\n\n"
                    f"Ученые доказали, что этот продукт повышает уровень счастья на 1000%. Почему? "
                    f"Да потому что: {product_desc}! Хватит откладывать жизнь на завтра, пора баловать себя.\n\n"
                    f"🔥 Аттракцион невиданной щедрости — отдаем {price_part}! Пока все не расхватали, беги оформлять! 🏃‍♂️💨"
                )

    return render_template(
        'index.html', 
        post_text=post_text, 
        error_message=error_message,
        product_name=product_name,
        product_desc=product_desc,
        product_price=product_price,
        selected_mood=selected_mood
    )

if __name__ == '__main__':
    app.run(debug=True)
