import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MODELS = {
    "apple": [
        "iPhone 11", "iPhone 11 Pro", "iPhone 11 Pro Max",
        "iPhone 12", "iPhone 12 Pro", "iPhone 12 Pro Max",
        "iPhone 13", "iPhone 13 Pro", "iPhone 13 Pro Max",
        "iPhone 14", "iPhone 14 Pro", "iPhone 14 Pro Max",
        "iPhone 15", "iPhone 15 Pro", "iPhone 15 Pro Max"
    ],
    "samsung": [
        "Galaxy A34 / A54 / A55", 
        "Galaxy S21 Ultra", "Galaxy S22 Ultra", 
        "Galaxy S23 Ultra", "Galaxy S24 Ultra",
        "Galaxy Note 10 / Note 20 Ultra"
    ],
    "xiaomi": [
        "Redmi Note 11 Pro", "Redmi Note 12 Pro", "Redmi Note 13 Pro",
        "POCO X3 Pro", "POCO X5 Pro", "POCO X6 Pro",
        "POCO F3 / F4 / F5 / F6", 
        "Xiaomi 13 / 13T / 14"
    ],
    "realme": ["Realme 9 Pro+", "Realme 11 Pro+", "Realme GT Neo 5"],
    "infinix": ["Infinix Note 30", "Tecno Pova 5"]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🍎 Apple", callback_data="brand_apple"),
            InlineKeyboardButton("📱 Samsung", callback_data="brand_samsung"),
        ],
        [
            InlineKeyboardButton("🟠 Xiaomi / POCO", callback_data="brand_xiaomi"),
            InlineKeyboardButton("🟡 Realme", callback_data="brand_realme"),
        ],
        [
            InlineKeyboardButton("⚡ Infinix / Tecno", callback_data="brand_infinix")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_text = "🎯 *Pro Sens Botiga Xush Kelibsiz!*\n\nIltimos, qurilmangiz brendini tanlang:"
    
    if update.message:
        await update.message.reply_text(msg_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(msg_text, reply_markup=reply_markup, parse_mode="Markdown")

async def brand_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    brand = query.data.split("_")[1]
    context.user_data['brand'] = brand
    
    keyboard = []
    row = []
    for idx, model in enumerate(MODELS[brand]):
        row.append(InlineKeyboardButton(model, callback_data=f"model_{idx}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_brand")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("📱 Aniq modelni tanlang:", reply_markup=reply_markup)

async def model_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    model_idx = int(query.data.split("_")[1])
    brand = context.user_data.get('brand')
    selected_model = MODELS[brand][model_idx]
    context.user_data['model'] = selected_model
    
    keyboard = [
        [InlineKeyboardButton("⚡ Giroskopli (Gyro)", callback_data="gyro_on")],
        [InlineKeyboardButton("🎯 Giroskopsiz (Non-Gyro)", callback_data="gyro_off")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"brand_{brand}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📱 Tanlangan model: *{selected_model}*\n\nGiroskop rejimini tanlang:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def gyro_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    is_gyro = query.data == "gyro_on"
    selected_model = context.user_data.get('model', 'Qurilma')
    
    if is_gyro:
        text = (
            f"🎯 *OPTIMAL SEZGIRLIK SOZLAMALARI*\n"
            f"📱 *Model:* {selected_model}\n"
            f"⚡ *Rejim:* Giroskopli (Gyro)\n\n"
            f"📷 *CAMERA SOZLAMALARI:*\n"
            f"• 3rd Person No Scope: *120%*\n"
            f"• 1st Person No Scope: *104%*\n"
            f"• Red Dot / Holo: *55%*\n"
            f"• 2x Scope: *38%*\n"
            f"• 3x Scope: *28%*\n"
            f"• 4x Scope: *20%*\n\n"
            f"🎯 *ADS SOZLAMALARI:*\n"
            f"• Red Dot / Holo: *60%*\n"
            f"• 3x Scope: *30%*\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *Camera va ADS tugadi. Giroskop sozlamalari:*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌀 *GIROSKOP SOZLAMALARI:*\n"
            f"• Gyroscope 3rd Person: *380%*\n"
            f"• Gyroscope Red Dot: *350%*\n"
            f"• Gyroscope 3x Scope: *300%*\n"
            f"• Gyroscope 4x Scope: *240%*"
        )
    else:
        text = (
            f"🎯 *OPTIMAL SEZGIRLIK SOZLAMALARI*\n"
            f"📱 *Model:* {selected_model}\n"
            f"🎯 *Rejim:* Giroskopsiz (Non-Gyro)\n\n"
            f"📷 *CAMERA & ADS SOZLAMALARI:*\n"
            f"• 3rd Person No Scope: *135%*\n"
            f"• 1st Person No Scope: *115%*\n"
            f"• Red Dot / Holo (ADS): *70%*\n"
            f"• 2x Scope (ADS): *50%*\n"
            f"• 3x Scope (ADS): *38%*\n"
            f"• 4x Scope (ADS): *28%*\n"
            f"• 6x Scope (ADS): *18%*"
        )
    
    keyboard = [[InlineKeyboardButton("🔄 Qaytadan hisoblash", callback_data="back_to_brand")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

if __name__ == '__main__':
    TOKEN = "8917450982:AAHvkw_RCMwtuYyKgdlGYGLKLLnArcyPIC8"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="^back_to_brand$"))
    app.add_handler(CallbackQueryHandler(brand_selected, pattern="^brand_"))
    app.add_handler(CallbackQueryHandler(model_selected, pattern="^model_"))
    app.add_handler(CallbackQueryHandler(gyro_selected, pattern="^gyro_"))
    
    print("Bot ishga tushdi...")
    app.run_polling()
