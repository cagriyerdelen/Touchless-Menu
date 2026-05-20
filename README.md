# Touchless-Menu
BL242 Görüntü İşleme dersi kapsamında geliştirilen, MediaPipe ve OpenCV tabanlı, gerçek zamanlı el takibi ve Pinch-Click (parmak tıklama) teknolojisi ile çalışan, menü navigasyonu ve sipariş yönetimi sağlayan temassız restoran otomasyonu.

1. Amaç 
Bu proje kapsamında, temassız ve hijyenik bir restoran sipariş deneyimi sunmak amacıyla bilgisayarlı görü tabanlı bir "Touchless Menu" (Temassız Menü) otomasyonu geliştirilmiştir. Günümüzde fiziksel temasın en aza indirilmesi gereken alanlarda, kullanıcıların herhangi bir fiziksel arayüze (dokunmatik ekran, buton vb.) ihtiyaç duymadan, sadece el hareketleri ile menü seçimi yapabilmesi ve siparişlerini yönetebilmesi hedeflenmiştir. Sistem, gerçek zamanlı görüntü işleme tekniklerini kullanarak insan-bilgisayar etkileşimini pratik bir uygulama senaryosuna dönüştürmektedir. 


2. Kullanılan Yöntem 
Proje geliştirilirken Python programlama dili ve OpenCV kütüphanesi temel alınmıştır. El tespiti ve takip süreçleri için Google MediaPipe çözümleri kullanılmıştır. Yöntemin teknik adımları şu şekildedir:  
Görüntü İşleme: Web kamerasından alınan görüntüler, MediaPipe kütüphanesi aracılığıyla anlık olarak işlenmiş ve el iskelet yapısı (hand landmarks) tespit edilmiştir.  
Etkileşim (Pinch Detection): Kullanıcının işaret parmağı ucu (landmark 8) ve başparmak ucu (landmark 4) arasındaki Öklid mesafesi hesaplanmıştır. Bu mesafe belirli bir eşik değerin (threshold) altına düştüğünde, sistem bunu bir "tıklama" aksiyonu olarak tanımlamıştır.  
Arayüz Yönetimi: OpenCV'nin grafik çizim fonksiyonları (cv2.rectangle, cv2.putText) kullanılarak dinamik bir menü sistemi oluşturulmuştur. Kullanıcı arayüzünde "Ana Menü", "Sipariş Sepeti" ve "Sipariş Özet" olmak üzere farklı sahneler arası geçişler, imleç koordinatları ve butonların sınırlayıcı kutuları (bounding box) kontrol edilerek sağlanmıştır. 

 
3. Elde edilen sonuçlar 
Geliştirilen uygulama, gerçek zamanlı olarak 25-30 FPS civarında stabil bir performans ile çalışmaktadır. Elde edilen temel bulgular şunlardır:  
Kullanılabilirlik: Kullanıcılar, fiziksel bir temas kurmadan menü içerisinde gezinme, ürün ekleme, sepeti düzenleme ve siparişi onaylama işlemlerini başarıyla tamamlayabilmektedir.  
Geri Bildirim: Sistem, sipariş onaylandığında kullanıcıya hem görsel (başarı ekranı) hem de işitsel (bip sesi) geri bildirimler sunarak etkileşimi güçlendirmiştir.  
Özgünlük: Geleneksel klavye/mouse odaklı sistemlerin aksine, bu proje tamamen jest tabanlı bir etkileşim modeli sunarak dönem boyunca öğrenilen görüntü işleme tekniklerini (nesne tespiti, takip, hareket analizi) bütünleşik bir sistemde uygulamıştır. 
