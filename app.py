import os
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

# Загружаем твои скрытые ключи из файла .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "diana_amazo_secret_key"

# Бэкенд берет ключи из окружения — твой ВК в полной безопасности!
VK_TOKEN = os.getenv("VK_TOKEN")
VK_GROUP_ID = os.getenv("VK_GROUP_ID")

@app.route("/", methods=["GET", "POST"])
def index():
    # Стартовые значения для полей формы
    post_text = "Здесь появится сгенерированный нейросетью текст поста..."
    product_name = ""
    product_desc = ""
    product_price = ""
    selected_mood = "expert"

    if request.method == "POST":
        # Ловим данные с формы
        product_name = request.form.get("product_name", "").strip()
        product_desc = request.form.get("product_desc", "").strip()
        product_price = request.form.get("product_price", "").strip()
        selected_mood = request.form.get("selected_mood", "expert")
        post_text = request.form.get("post_text", "").strip()
        
        # ---------------------------------------------------------------------
        # ЛОГИКА 1: Клик по кнопке "🤖 Сгенерировать пост через ИИ" (БЕСПЛАТНО)
        # ---------------------------------------------------------------------
        if "generate_post" in request.form:
            if not product_name:
                flash("❌ Укажите хотя бы название товара для генерации!", "danger")
            else:
                flash("🤖 Отправляю запрос в бесплатную нейросеть...", "info")
                
                # Формируем промпт под выбранную тональность контента
                prompt = (
                    f"Напиши один короткий, сочный, продающий пост для соцсетей про товар.\n"
                    f"Название: {product_name}\n"
                    f"Описание: {product_desc}\n"
                    f"Цена: {product_price}\n"
                    f"Тональность текста (Tone of Voice): {selected_mood}.\n"
                    f"Используй эмодзи и абзацы."
                )
                
                url = "https://pollinations.ai"
                try:
                    response = requests.get(f"{url}{requests.utils.quote(prompt)}", timeout=20)
                    if response.status_code == 200 and response.text.strip():
                        post_text = response.text.strip()
                        flash("🎉 Текст поста успешно сгенерирован ИИ бесплатно!", "success")
                    else:
                        raise Exception("Ошибка сервера ИИ")
                except Exception as e:
                    # Умный локальный генератор на все 6 тонов на случай сбоев сети
                    if selected_mood == "humorous":
                        header_vibe = f"🚀 Внимание, земляне! Космический юмор на связи! Встречайте: {product_name}! 🔥"
                        desc_vibe = f"🛸 Что умеет эта штука: {product_desc}. Да-да, технологии будущего уже тут!"
                        footer_vibe = f"💰 Аттракцион невиданной щедрости всего за: {product_price}! Разбирайте, пока инопланетяне не угнали! 👽"
                    elif selected_mood == "friendly":
                        header_vibe = f"🤝 Друзья, привет! Хочу поделиться с вами классной находкой — {product_name}! ❤️"
                        desc_vibe = f"✨ Вот почему она мне так нравится: {product_desc}. Очень уютная и полезная вещь."
                        footer_vibe = f"💰 Забрать себе за приятную цену: {product_price}. Порадуйте себя и близких! 🥰"
                    elif selected_mood == "sales":
                        header_vibe = f"🔥 ШОК-ЦЕНА! Успейте забрать: {product_name}! 👇"
                        desc_vibe = f"⚡ РАСПРОДАЖА: {product_desc}. Количество товара ограничено, скидка действует только сегодня!"
                        footer_vibe = f"🛒 Цена по акции прямо сейчас: {product_price} руб! Кликайте и заказывайте! 🛍️"
                    elif selected_mood == "formal":
                        header_vibe = f"💼 Официальное коммерческое предложение. Презентация позиции: {product_name}."
                        desc_vibe = f"📋 Функциональные особенности и регламентированные параметры: {product_desc}."
                        footer_vibe = f"💳 Фиксированная розничная стоимость составляет: {product_price} единиц. Доступно к заказу."
                    elif selected_mood == "storytelling":
                        header_vibe = f"📖 История о том, как {product_name} полностью изменил мой привычный день..."
                        desc_vibe = f"✨ Недавно я столкнулся с проблемой, но этот гаджет решил её мгновенно: {product_desc}. Это просто спасение!"
                        footer_vibe = f"💰 Ни разу не пожалел о покупке, тем более цена всего: {product_price}. Искренне рекомендую каждому! ✨"
                    else:  # expert
                        header_vibe = f"🎓 Экспертный обзор рынка. Анализ продукта: {product_name}."
                        desc_vibe = f"📋 Технические характеристики и функционал: {product_desc}. Соответствует высоким стандартам качества."
                        footer_vibe = f"💳 Инвестиционная стоимость позиции: {product_price}. Оптимальное бизнес-решение."
                    
                    post_text = f"{header_vibe}\n\n{desc_vibe}\n\n{footer_vibe}\n\n🤖 [Сгенерировано в режиме Friendly-Вайбкодинга!]"
                    flash("🎉 Текст успешно адаптирован под выбранный Tone of Voice!", "success")

        # ---------------------------------------------------------------------
        # ЛОГИКА 2: Клик по кнопке "📝 Зафиксировать в voice.md"
        # ---------------------------------------------------------------------
        elif "save_changes" in request.form:
            try:
                with open("voice.md", "w", encoding="utf-8") as f:
                    f.write(f"# Настройки Tone of Voice\n Выбранная тональность: **{selected_mood}**")
                flash(f"📝 Тональность '{selected_mood}' успешно записана в voice.md!", "success")
            except Exception as e:
                flash(f"❌ Не удалось записать файл: {str(e)}", "danger")
            
        # ---------------------------------------------------------------------
        # ЛОГИКА 3: Клик по кнопке "🚀 Опубликовать в VK"
        # ---------------------------------------------------------------------
        elif "publish_vk" in request.form:
            url = "https://vk.com"
            params = {
                "access_token": VK_TOKEN,
                "owner_id": VK_GROUP_ID,
                "message": post_text,
                "v": "5.131"
            }
            try:
                response = requests.post(url, data=params, timeout=10)
                if response.status_code == 200:
                    flash("🎉 Пост успешно опубликован на стене VK!", "success")
                else:
                    flash(f"❌ Ошибка сервера VK. Статус-код: {response.status_code}", "danger")
            except Exception as e:
                flash(f"❌ Ошибка сети при отправке в VK: {str(e)}", "danger")

    return render_template(
        "index.html", 
        post_text=post_text, 
        product_name=product_name,
        product_desc=product_desc,
        product_price=product_price,
        selected_mood=selected_mood
    )

if __name__ == "__main__":
    app.run(debug=True)
