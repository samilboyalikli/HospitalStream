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

