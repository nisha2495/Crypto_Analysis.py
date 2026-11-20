import tkinter as tk
from tkinter import scrolledtext
import requests
import numpy as np
from datetime import datetime

# ===== LLM AGENT BRAIN =====
class CryptoAgent:
    def get_price(self, coin):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true"
            d = requests.get(url, timeout=10).json()[coin]
            return d
        except:
            return None

    def get_history(self, coin, days=30):
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}"
            d = requests.get(url, timeout=10).json()
            return [p[1] for p in d['prices']]
        except:
            return []

    def get_top_coins(self):
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
            return requests.get(url, timeout=10).json()
        except:
            return []

    def answer(self, question):
        q = question.lower()
        
        # 1. TOP COINS
        if "top" in q or "best" in q or "behtareen" in q or "sab se" in q:
            coins = self.get_top_coins()
            ans = "🏆 TOP 5 Cryptocurrency (Market Cap ke hisab se):\n\n"
            for i, c in enumerate(coins, 1):
                ans += f"{i}. {c['name']} ({c['symbol'].upper()}) - ${c['current_price']:,.2f} | 24h: {c['price_change_percentage_24h']:.2f}%\n"
            ans += "\n💡 Agent Advice: Top coin ka matlab safe hai, lekin profit chhote coin me zyada hota hai."
            return ans

        # 2. COMPARE - Bitcoin vs Ethereum
        if "vs" in q or "compare" in q or "ya" in q and "behtar" in q:
            # Bitcoin vs Ethereum nikaalo
            b = self.get_price("bitcoin")
            e = self.get_price("ethereum")
            if b and e:
                return f"⚔️ COMPARISON - LLM Agent Analysis:\n\nBitcoin: ${b['usd']:,.2f} | 24h Change: {b['usd_24h_change']:.2f}%\nEthereum: ${e['usd']:,.2f} | 24h Change: {e['usd_24h_change']:.2f}%\n\n🧠 Agent Ka Faisla:\n{'Bitcoin zyada strong hai aaj' if b['usd_24h_change'] > e['usd_24h_change'] else 'Ethereum zyada strong hai aaj'} kyunki uska 24h change behtar hai.\n\nBitcoin = Digital Gold (Safe)\nEthereum = Smart Contracts (Growth)"
            return "Compare nahi ho saka, internet check karo"

        # 3. KISI EK COIN KA ANALYSIS
        coin_map = {"bitcoin":"bitcoin","btc":"bitcoin","ethereum":"ethereum","eth":"ethereum","dogecoin":"dogecoin","doge":"dogecoin","solana":"solana","sol":"solana","cardano":"cardano","ada":"cardano"}
        found = None
        for k,v in coin_map.items():
            if k in q:
                found = v
                break
        
        if found:
            price_data = self.get_price(found)
            hist = self.get_history(found, 30)
            if price_data and hist:
                price = price_data['usd']
                change = price_data['usd_24h_change']
                vol = price_data['usd_24h_vol']
                cap = price_data['usd_market_cap']
                # Prediction
                x = np.arange(len(hist)); y = np.array(hist)
                m,b = np.polyfit(x,y,1)
                tomorrow = m*(len(hist)+1)+b
                trend = "UP ⬆️" if m>0 else "DOWN ⬇️"
                return f"🤖 LLM AGENT REPORT: {found.upper()}\n{'='*40}\n\n💰 Live Price: ${price:,.2f}\n📈 24h Change: {change:.2f}%\n💵 24h Volume: ${vol:,.0f}\n🏦 Market Cap: ${cap:,.0f}\n\n📊 30-Din Analysis:\nTrend: {trend}\nHighest (30 din): ${max(hist):,.2f}\nLowest (30 din): ${min(hist):,.2f}\nAverage: ${np.mean(hist):,.2f}\n\n🔮 Kal Ki Prediction: ${tomorrow:,.2f}\n\n💡 Agent Advice: {'Trend UP hai, Hold karo / Buy socho' if m>0 else 'Trend DOWN hai, Wait karo, panic me Sell mat karo'}\n\nSource: Live CoinGecko Data"
        
        # 4. DEFAULT
        return "🤖 Me tumhara Crypto Data Agent hun! Mujhse ye poocho:\n\n1. 'Bitcoin ka analysis karo'\n2. 'Top 5 coins dikhao'\n3. 'Bitcoin vs Ethereum kaunsa behtar hai?'\n4. 'Ethereum ka price kya hai?'\n\nKuch bhi likho, me data se jawab dunga!"

# ===== UI =====
class App:
    def __init__(self, root):
        self.agent = CryptoAgent()
        root.title("LLM-Powered Crypto Data Analysis Agent - By Nisha")
        root.geometry("900x600")
        root.configure(bg="#0F172A")

        tk.Label(root, text="🤖 LLM-Powered Data Analysis Agent", font=("Arial", 20, "bold"), bg="#0F172A", fg="white").pack(pady=10)
        tk.Label(root, text="Cryptocurrency Analysis | Apne Data Se Baat Karo!", font=("Arial", 11), bg="#0F172A", fg="#38BDF8").pack()

        self.chat = scrolledtext.ScrolledText(root, height=15, font=("Arial", 11), bg="#1E293B", fg="white", wrap="word")
        self.chat.pack(padx=20, pady=15, fill="both", expand=True)
        self.chat.insert("end", "🤖 Agent: Assalam-o-Alaikum Nisha! Me tumhara Crypto Agent hun. Mujhse poocho - 'Bitcoin ka analysis karo'\n\n")
        self.chat.config(state="disabled")

        # Quick Buttons
        btn_frame = tk.Frame(root, bg="#0F172A")
        btn_frame.pack(pady=5)
        for txt in ["Bitcoin ka analysis karo", "Top 5 coins dikhao", "Bitcoin vs Ethereum"]:
            tk.Button(btn_frame, text=txt, bg="#22C55E", fg="white", font=("Arial", 10, "bold"), command=lambda t=txt: self.send(t)).pack(side="left", padx=5)

        bottom = tk.Frame(root, bg="#0F172A")
        bottom.pack(pady=10, fill="x", padx=20)
        self.entry = tk.Entry(bottom, font=("Arial", 12), width=50)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.send())
        tk.Button(bottom, text="Send ➤", bg="#38BDF8", fg="white", font=("Arial", 11, "bold"), command=self.send).pack(side="left", padx=10)

    def send(self, text=None):
        q = text if text else self.entry.get()
        if not q.strip(): return
        self.entry.delete(0, "end")
        self.chat.config(state="normal")
        self.chat.insert("end", f"\n🧑 Tum: {q}\n")
        self.chat.insert("end", "🤖 Agent soch raha hai...\n")
        self.chat.see("end")
        self.chat.update()
        ans = self.agent.answer(q)
        # Remove "soch raha" line
        self.chat.delete("end-2l", "end-1l")
        self.chat.insert("end", f"🤖 Agent:\n{ans}\n{'='*50}\n")
        self.chat.config(state="disabled")
        self.chat.see("end")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()