# HOSPITAL SIMULATION
13 Hastanenin Canlı Veri Akışının Basit Bir Simülasyonu.
## Genel Bakış
Hastane Simülasyonu, hastanelerin canlı veri akışının küçük bir kısmını simüle eder. Orkestrasyon için docker-compose kullanan sistem, sahte verileri üretirken Apache Spark'ın batch yapısını kullanır. Ürettiği verilerden Apache Kafka vasıtasıyla bir veri akışı oluşturur ve bunları iki katmanda analiz eder. ilk katmanda Apache Kafka'yı kullanırken ikinci katmanda Apache Spark'ın Structured Streaming yapısını kullanır.
## Projenin Amacı
Apache Spark üzerinde çalışırken canlı veri çekebileceğim ve internet stabilitesi, siber güvenlik, öngörülebilir karmaşıklık gibi parametreleri düşündürmeyecek veri akışları bulmakta oldukça zorlandım. Bunun sonucunda kendim Apache Spark'ın batch modüllerini kullanarak sahte veriler üretmeye başladım. Bunları da bir veri akışı oluşturacak  biçimde programlayıp üzerine Apache Spark'ın Structured Streaming modülüyle bazı analizler yazdım.

Projenin amacı, en düşük risk ve karmaşıklıkla canlı veri akışı simüle etmektir. İkincil olarak, bu veriler üzerinde en basitten başlayıp en karmaşığa doğru çeşitli canlı analizler oluşturarak, Apache Kafka'yı ve Apache Spark'ı anlamaktır. Tüm bu işlemleri de Docker ile orkestre ederek docker-compose üzerinde derin bir kavrayış kazanmaktır.
## Alternatif Kullanımlar
Eğer;
1. Gerçek Zamanlı bir veri akışı oluşturmak istiyorsanız.
2. Gerçek Zamanlı bir veri akışı üzerinde analiz denemek istiyorsanız.
3. Docker-compose'un çalışma biçimini anlamak istiyorsanız.
4. Apache Spark'la sahte veri üretmek istiyorsanız.
5. Apache Kafka ile canlı bir veri akışı üzerinde analizler yazmak istiyorsanız.

bu simülasyon işinizi görecektir.
## Simülasyonun Şeması
![Main Schema of Project.](/assets/main_schema.jpeg "TMain Schema of Project.")

### Producer

Bu kısımda, sahte veriler üretiyoruz ve bu verileri Raw Stream adı verdiğimiz bir canlı veri akışına gönderiyoruz. Verileri oluştururken Apache Spark kullanıyoruz. Buradaki işlemler proje kaynak kodlarındaki hospitals dizini ile yapılıyor.

Producer Files: 
```
hospitals  
    ├─ atlanta.py  
    ├─ boston.py  
    ├─ chicago.py  
    ├─ dallas.py  
    ├─ detroit.py  
    ├─ Dockerfile  
    ├─ gender_name.csv
    ├─ houston.py  
    ├─ jersey.py  
    ├─ last_name.csv  
    ├─ miami.py  
    ├─ newyork.py  
    ├─ phoenix.py  
    ├─ requirements.txt
    ├─ sanfrancisco.py
    ├─ seattle.py  
    └─ washington.py
```


### Raw Stream

![Raw Stream Topic.](/assets/raw_stream.png "Raw Stream Topic.")

Oluşturulan veriler Apache Kafka kullanılarak raw_stream adında bir topic'e yazılıyor. Böylece tüm ham veriler kolaylıkla bu topicten olduğu gibi -analiz edilmeden- okunabiliyor ve üzerlerinde alternatif kodlamalar yapılabiliyor.

### Analyzer

Projenin bu kısmı üç temel misyonu yerine getirir. 
1. Topics dizinindeki distributor dizini ile Raw Stream'deki verileri okur. Ardından okuduğu verileri yaşlarına göre children topic'ine, adult topic'ine veya senior topic'ine yazar.
2. children, adult ve senior topiclerindeki verileri topics dizini ile analiz eder ve sonuçlar üreterek, verileri flagler.
3. flaglediği verileri, topics dizini ile analyzed_stream topic'ine gönderir.

Analyzer Files: 
```
distributor
    ├─ distributor.py
    ├─ Dockerfile
    └─ requirements.txt

topics
    ├─ adult
    │   ├─ Dockerfile
    │   ├─ entrypoint.sh
    │   └─ main.py
    ├─ children
    │   ├─ Dockerfile
    │   ├─ entrypoint.sh
    │   └─ main.py
    └─ senior
        ├─ Dockerfile
        ├─ entrypoint.sh
        └─ main.py
```

### Analyzed Stream

![Analyzed Stream Topic.](/assets/analyzed_stream.png "Analyzed Stream Topic.")

Flaglenen veriler Apache Kafka kullanılarak analyzed_stream adında bir topic'e yazılır. Burada artık veriler işlenmiş ve raporlanmış bir biçimde yer almaktadır ve kullanıcı okunmasına hazırdır. Ancak elbette veri görselleştirmesi için bir consumer yazılması verilerin okunabilirliğini artıracaktır. Bunun içinde bir consumer hazırladım.


### Consumer

Adından da anlaşılacağı üzere consumer dizininde kodladığım, analiz edilmiş verileri görmemizi ve basit bir terminal görselleştirmesi sunmamızı sağlayan kısım. Burada flaglenmiş veriler, topics tarafından kendilerine yapıştırılan flaglere göre renklendirilir ve konsola yazılır. Böylece kullanıcı verileri analiz edilmiş bir biçimde görme fırsatı elde eder.

Consumer Files: 
```
consumer
    ├─ Dockerfile
    ├─ main.py
    └─ requirements.txt
```

## Topics
![Main Schema of Project.](/assets/topic_schema.jpeg "TMain Schema of Project.")

Projede sadece 5 Apache Kafka topic'i bulunuyor. 

- Raw Stream topic'i işlenmemiş verileri barındırıyor. 
- Children topic'i Raw Stream topic'inde yaşı 18'in altındaki kayıtları barındırıyor. 
- Adult topic'i Raw Stream topic'inde yaşı 18 ile 65 arasındaki kayıtları barındırıyor. 
- Senior topic'i ise Raw Stream topic'inde bulunan 65 yaşının üstündeki kayıtları barındırıyor.
- Analyzed Stream topic'i Raw Stream topic'indeki verilerin analiz edilmiş sonuçlarını barındırıyor.

## Sahte Verilerin Anatomisi

Her bir veri, hastanede kan testi yaptıran hasta kaydını temsil eder. Her biri dictionary ögesidir. En başta 8 key'den ve 8 value'den oluşurken sonradan bu sayı flagler ile birlikte artış göstermektedir. Aşağıda Raw Stream verilerinin açıklaması, bloodValues ögesindeki key-value çiftlerinin anlamları ve Analyzed Stream verilerinin açıklamaları yer almaktadır.

#### Raw Stream:
```Py
"Name":"hasta_adi",
"Surname":"hasta_soyadi",
"Age":hasta_yasi,
"cbc":"hasta_yas_araligi",
"bloodValues":{hasta_kan_degerleri},
"Hospital":"test_yapilan_hastane",
"Gender":"hasta_cinsiyeti",
"Time":verinin_sisteme_giris_zamani
```

- Name, hastanın adıdır (string).  
- Surname hastanın soyadıdır (string).  
- Age hastanın yaşıdır (integer).  
- cbc hastanın yaş aralığıdır (string) -Dipnot: Bu kısım geliştirme esnasındaki bazı kolaylıklardan dolayı konulmuştur, kaldırılacaktır.- (string).  
- bloodValues hastanın kan değerlerini içeren bir başka dictionary ögesidir -Bu kısım aşağıda ayrıntılı açıklanacaktır.- (dictionary).  
- Hospital hastanın kan testini yaptırdığı hastanenin adıdır (string).  
- Gender hastanın cinsiyetidir (string).  
- Time hastanın kan testinin sisteme yüklendiği zamandır -Bir başka deyişle, producer'ın sahte veriyi ürettiği zamandır.- (timestamp). 

#### `bloodValues` Çiftlerinin Anlamları:
```Py
"WBC":beyaz_kan_hucreleri-lokositler,
"RBC":kirmizi_kan_hucreleri-eritrositler,
"Hb":hemoglobin,
"Hct":"hematokrit%",
"MCV":ortalama_eritrosit_hacmi,
"MCH":ortalama_hemoglobin_miktari,
"MCHC":"ortalama_hemoglobin_konsantrasyonu%"
```

- WBC (White Blood Cell, Beyaz Kan Hücreleri - Lökositler), bağışıklık sisteminin bir parçasıdır. Vücuda giren enfeksiyonlarla savaşır. Düşükse bağışıklık zayıflamış olabilir, yüksekse enfeksiyon veya iltihap belirtisi olabilir.
- RBC (Red Blood Cell, Kırmızı Kan Hücreleri - Eritrositler), oksijen taşıyan hücrelerdir. Düşüklüğü anemiye, fazlalığı bazı kan hastalıklarına işaret edebilir.
- Hb (Hemoglobin), kırmızı kan hücrelerinde bulunan, oksijen taşıyan proteindir. Düşük olması kansızlığı (anemi) gösterebilir.
- Hct (Hematocrit), Kanın ne kadarının kırmızı kan hücrelerinden oluştuğunu gösterir. Düşükse anemi, yüksekse sıvı kaybı veya bazı hastalıklar düşünülebilir.
- MCV (Mean Corpuscular Volume, Ortalama Eritrosit Hacmi), kırmızı kan hücrelerinin büyüklüğünü gösterir. Küçükse demir eksikliği, büyükse B12 veya folik asit eksikliği olabilir.
- MCH (Mean Corpuscular Hemoglobin, Ortalama Hemoglobin Miktarı), her kırmızı kan hücresinde ne kadar hemoglobin bulunduğunu gösterir. Düşüklük demir eksikliğini, yükseklik B12 eksikliğini gösterebilir.
- MCHC (Mean Corpuscular Hemoglobin Concentration, Ortalama Hemoglobin Konsantrasyonu), kırmızı kan hücrelerindeki hemoglobin yoğunluğunu gösterir. Düşüklüğü anemiye, yüksekliği bazı nadir kan hastalıklarına işaret edebilir.

#### Analyzed Stream:

```Py
"Name":"hasta_adi",
"Surname":"hasta_soyadi",
"Age":hasta_yasi,
"bloodValues":{hasta_kan_degerleri},
"Hospital":"test_yapilan_hastane",
"Gender":"hasta_cinsiyeti",
"Time":verinin_sisteme_giris_zamani,
"status(WBC)":wbc_analiz_sonucu,
"status(RBC)":rbc_analiz_sonucu,
"status(Hb)":hb_analiz_sonucu,
"status(Hct)":hct_analiz_sonucu,
"status(MCV)":mcv_analiz_sonucu,
"status(MCH)":mch_analiz_sonucu,
"status(MCHC)":mchc_analiz_sonucu
```

- `Status(WBC)`, WBC analizinin sonucunu ifade eder. 0-2 yaş çocuklar için ideal olan 6000-17500 arasıdır. 2-12 yaş çocuklar için 5000-15000 arası ve 12-18 yaş çocuklar için ideal aralık 4500-13500 arasıdır. **TODO:ADULT&SENIOR** İdeal aralıklarda olan WBC için Status(WBC) flag'i `True` olarak işaretlenir, aksi durumda `False` olur (bool).

- `Status(RBC)`, RBC analizinin sonucunu ifade eder. 0-2 yaş çocuklar için ideal olan 3900000-5500000 arasıdır. 2-12 yaş çocuklar için 4000000-5200000 arası ve 12-18 yaş çocuklar için ideal aralık 4100000-5600000 arasıdır. **TODO:ADULT&SENIOR** İdeal aralıklarda olan RBC için Status(RBC) flag'i `True` olarak işaretlenir, aksi durumda `False` olur (bool).

- `Status(Hb)`, Hb analizinin sonucunu ifade eder. 0-2 yaş çocuklar için ideal olan 10.0-14.0 arasıdır. 2-12 yaş çocuklar için 11.5-15.5 arası ve 12-18 yaş çocuklar için ideal aralık kız ve erkek çocuklar için değişmektedir. Kız çocuklar için ideal aralık 12.0-15.0 iken, erkek çocuklarda bu aralık 13.0-16.0'dır. **TODO:ADULT&SENIOR** İdeal aralıklarda olan Hb için Status(Hb) flag'i `True` olarak işaretlenir, aksi durumda `False` olur (bool).

- `Status(Hm)`, Hm analizinin sonucunu ifade eder. 0-2 yaş çocuklar için ideal olan %33-%43 arasıdır. 2-12 yaş çocuklar için %34-%42 arası ve 12-18 yaş çocuklar için ideal aralık kız ve erkek çocuklar için değişmektedir. Kız çocuklar için ideal aralık %36-%45 iken, erkek çocuklarda bu aralık %40-%50'dır. **TODO:ADULT&SENIOR** İdeal aralıklarda olan Hm için Status(Hm) flag'i `True` olarak işaretlenir, aksi durumda `False` olur (bool).

- `Status(MCV)`, MCV analizinin sonucunu ifade eder. 0-2 yaş çocuklar için ideal olan 70-86 arasıdır. 2-12 yaş çocuklar için 75-87 arası ve 12-18 yaş çocuklar için ideal aralık 80-96 arasıdır. **TODO:ADULT&SENIOR** İdeal aralıklarda olan MCV için Status(MCV) flag'i `True` olarak işaretlenir, aksi durumda `False` olur (bool).

- `Status(MCH)`, MCH analizinin sonucunu ifade eder. 0-2 yaş çocuklar için ideal olan 24-30 arasıdır. 2-12 yaş çocuklar için 26-32 arası ve 12-18 yaş çocuklar için ideal aralık 28-34 arasıdır. **TODO:ADULT&SENIOR** İdeal aralıklarda olan MCH için Status(MCH) flag'i `True` olarak işaretlenir, aksi durumda `False` olur (bool).

- `Status(MCHC)`, MCHC analizinin sonucunu ifade eder. 0-2 yaş çocuklar için ideal oran %30-%36 arasıdır. 2-18 yaş çocuklar için ise ideal oran %32-%36'dır. **TODO:ADULT&SENIOR** İdeal aralıklarda olan MCHC için Status(MCHC) flag'i `True` olarak işaretlenir, aksi durumda `False` olur (bool).
