The social media scraping  with text polarity detections.

The text sentiment polarity score is a float within the range [-1.0, 1.0].

-1.0 .. -0.65 - angry
-0.65 .. 0.5  - neutral
0.5 .. 1      - happy


 The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
 
 All the non english text will be translated into english.
 
 (using TextBlob python library)

 
 output example in JSON format:
 
 {
  "_index": "index1",
  "_type": "twitter",
  "_id": "884672401140838400",
  "_version": 2,
  "_score": null,
  "_source": {
    "author": "NovoNews",
    "screen_name": "NovoNews",
    "location": "Riga, Latvia",
    "coords": {
      "lat": 0,
      "lon": 0
    },
    "text": "Ждем от наших игроков хорошего хоккея! https://t.co/HaqjDPhdKb",
    "text_en": "Looking forward to our players have a good hockey! Https://t.co/HaqjDPhdKb",
    "sentiment_pol": "0.875",
    "str_polarity": "happy",
    "sentiment_sub": "0.600",
    "detect_lang": "ru",
    "timestamp": "2017-07-11T07:15:11Z"
  },
  "fields": {
    "timestamp": [
      1499757311000
    ]
  },
  "highlight": {
    "detect_lang.keyword": [
      "@kibana-highlighted-field@ru@/kibana-highlighted-field@"
    ],
    "screen_name.keyword": [
      "@kibana-highlighted-field@NovoNews@/kibana-highlighted-field@"
    ],
    "str_polarity.keyword": [
      "@kibana-highlighted-field@happy@/kibana-highlighted-field@"
    ]
  },
  "sort": [
    1499757311000
  ]
}
