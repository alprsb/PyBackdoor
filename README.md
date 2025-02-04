# 🕵️ Python Backdoor - Ethical Hacking Tool  

Bu proje, **Python** kullanılarak geliştirilmiş bir **backdoor** uygulamasıdır. Client-server mimarisi ile çalışır ve **socket** modülü kullanarak bağlantı kurar. **Sadece eğitim ve test amaçlıdır.**  

## ⚙️ **Özellikler**  
✅ Client ve Server arasında şifrelenmemiş doğrudan bağlantı  
✅ Komut gönderme ve sonuçları alma  
✅ Dosya indirme & yükleme  
✅ Arka planda sessiz çalışma (Stealth Mode - İsteğe bağlı)  
✅ Bağlantı koparsa otomatik tekrar bağlanma  

## 📂 **Dosya Yapısı**  
📁 **client.py** → Hedef sistemde çalışacak olan istemci kodu  
📁 **socket.py** → Ana sunucu tarafı, bağlantıları yönetir  

## 🚀 **Kullanım Talimatları**  

### 1️⃣ **Server'ı (socket.py) Çalıştırın**  
Öncelikle sunucu tarafını dinlemeye alın:  

```bash
python socket.py

2️⃣ Client'ı (client.py) Hedef Sistemde Çalıştırın
Bağlantıyı başlatmak için client tarafını çalıştırın:
python client.py

⚠️ Yasal Uyarı
Bu araç yalnızca eğitim ve etik hacking amaçlı geliştirilmiştir. İzinsiz sistemlere erişmek yasa dışıdır ve cezai yaptırımlara tabidir. Geliştirici, yasadışı kullanımda sorumluluk kabul etmez.

