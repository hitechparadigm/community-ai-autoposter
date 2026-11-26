# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `217d6d8f` · 9/9 posts written · **5/9 passed every check** · 40 Claude calls · $0.58 ($0.064 per post)

| Check | Pass rate |
| --- | --- |
| facts | 89% |
| glossary | 100% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 89% |
| reviewer | 100% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 4.00 |
| language | 4.00 |
| usefulness | 3.78 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| akwesasne-policing | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| cra-ccb-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | 4/4/3 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/3 |

## Details

### min-wage-mb

**У Манітобі мінімальна зарплата зросте до 16,50 долара**

З 1 жовтня мінімальна оплата праці в Манітобі становитиме 16,50 долара за годину. Про це у вівторок оголосив уряд провінції. Ставка зросте на 65 центів.

Розмір мінімалки прив'язаний до інфляції в провінції — цього вимагає закон, ухвалений у 2023 році. Міністр праці Манітоби Деніел Моро (Daniel Moreau) повідомив, що мінімальну зарплату отримують близько 40 тисяч людей, здебільшого в роздрібній торгівлі та закладах харчування. «Родини досі відчувають, скільки коштують продукти й оренда, тож ця зміна дає змогу зарплатам іти в ногу з цінами», — сказав він на пресконференції у Вінніпегу.

Торгові палати Манітоби (Manitoba Chambers of Commerce) зазначили, що малий бізнес візьме нові витрати на себе, але попросили в майбутньому повідомляти роботодавців про зміни завчасніше. За їхніми словами, багато компаній і так платять більше за мінімальну ставку, щоб залучити працівників.

Ставка в Манітобі залишиться нижчою, ніж у Британській Колумбії, але вищою, ніж у Саскачевані. Роботодавці мають платити за новою ставкою за всі години, відпрацьовані від 1 жовтня, зокрема студентам і працівникам із неповним робочим днем.

Judge: Accuracy: "Торгові палати Манітоби" renders the singular organisation "Manitoba Chambers of Commerce" as plural chambers, which is a minor slip. "Близько 40 тисяч людей" omits "workers", but this is minor. Everything else matches: figures, date, 2023 law, minister, comparisons with BC and Saskatchewan.
Language: Mostly natural. "Мінімалка" is colloquial for a news post. "Візьме нові витрати на себе" is slightly awkward. "Повідомляти роботодавців" is a wrong construction and should be "повідомляти роботодавцям". "Платять більше за мінімальну ставку" should be "вище за / більше, ніж мінімальна ставка". "Іти в ногу з цінами" is fine. "Мають платити ... від 1 жовтня" is acceptable. Using "зарплата" and "оплата праці" together is fine.
Usefulness: Clear and complete, and it tells readers what changes and from when. It is slightly lacking in explaining the relevance to the Ukrainian community, and the "Про це у вівторок оголосив уряд" flow is a little choppy. Otherwise no padding.

### rcmp-deepfake

**Канадська королівська кінна поліція попереджає про любовні шахрайства з дипфейками в Метро-Ванкувері**

Канадська королівська кінна поліція (RCMP) попереджає мешканців Метро-Ванкувера про любовні афери, в яких шахраї видають себе за інших людей за допомогою відео, створеного штучним інтелектом.

Цього року 85 мешканців регіону повідомили, що втратили загалом 2,3 млн доларів. Зазвичай аферист знайомиться із жертвою в застосунку для побачень або в соцмережах, а потім влаштовує короткі відеодзвінки. Дипфейк підміняє обличчя й голос, і вигадана особа здається справжньою. Коли довіра встановлена, шахрай просить гроші: на лікування, через заблокований рахунок або для вигідного вкладення. «Дзвінки виглядають справжніми, саме тому ці схеми такі дієві», — каже сержантка Прія Сандху (Priya Sandhu) з відділу фінансових злочинів RCMP у місті Суррей (Surrey).

Про шахрайство можуть свідчити кілька ознак: співрозмовник не може зустрітися наживо, дзвінок раптово обривається, коли його просять повернути голову, а також будь-яке прохання про криптовалюту чи подарункові картки. Якщо ви вже надіслали гроші, одразу зв'яжіться з банком і повідомте місцеву поліцію та Канадський центр протидії шахрайству (Canadian Anti-Fraud Centre).

Judge: Accuracy: "для вигідного вкладення" adds "profitable", which the source doesn't say (it only says "an investment opportunity"). "на лікування" narrows "medical emergency", which is an urgent situation. "Investigators say" and "so far" are dropped, so the figures read as final totals for the year. "Frozen" account becomes "заблокований", which is acceptable. Language: mostly natural. "вкладення" is slightly awkward, and "заморожений рахунок" or "інвестиційна пропозиція" would be closer. The two paragraphs are dense, and the quote is buried in a long block. Usefulness: clear, with warning signs and what to do. The second paragraph would read better if split, and the quote would work better after the numbers.

### ucc-mentorship

**В Едмонтоні запустили програму наставництва для українців з CUAET**

Провінційна рада Конгресу українців Канади (КУК) в Альберті запустила в Едмонтоні програму наставництва для українців, які приїхали до Канади за програмою CUAET.

Новоприбулим допомагатимуть 120 волонтерів. Здебільшого це канадські українці, які працюють у кваліфікованих робітничих професіях, медицині та інженерії. Наставник зустрічається з підопічним щонайменше двічі на місяць упродовж пів року. Разом вони шукають роботу, домагаються визнання кваліфікації, підбирають житло в оренду й заповнюють урядові форми. Програму фінансує приватний фонд Prairie Bridges Foundation з Калгарі: він виділив 250 тисяч доларів на два роки.

Координаторка програми Галина Мороз (Halyna Moroz) каже, що багато людей приїхали з добрим фахом, але не знають, як усе влаштовано в Канаді, а підказати нікому. За її словами, наставник заощаджує місяці спроб і помилок. Заявки від новоприбулих і від охочих стати наставниками приймають до 15 січня. Наступного року рада планує поширити програму на Калгарі, якщо вистачить коштів.

Judge: Facts match the source: 120 mentors, twice a month for six months, $250,000 over two years, Calgary foundation, 15 January deadline, Calgary expansion. The glossary names are used correctly.

Language: "урядові форми" is a calque of "government forms". Better: "урядові бланки/формуляри" or "офіційні документи". "Галина Мороз (Halyna Moroz)" has an unnecessary Latin transliteration in parentheses. "домагаються визнання кваліфікації" is slightly off, because "домагатися" implies a struggle. "Здебільшого це канадські українці, які працюють у кваліфікованих робітничих професіях" is a bit clumsy. "Заощаджує місяці спроб і помилок" is acceptable but a little stiff.

Usefulness: the post is clear and relevant. It does not say how to apply or where to find the application. The source gives no such details, so this is only a minor limit. It paraphrases the quote rather than using it directly.

### ircc-cuaet-pr

**Українці, які приїхали за CUAET, зможуть подати заявку на постійне резидентство**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє нову програму постійного резидентства (PR) для українців, які приїхали до країни за програмою CUAET. Про це відомство повідомило в четвер.

Прийом заявок почнеться 2 березня. Міністерство прийме до 10 000 заявок. Щоб податися, потрібно мати щонайменше рік повного робочого стажу в Канаді, здобутого після приїзду за CUAET, і результат мовного тесту не нижчий за CLB 5 з англійської або NCLC 5 з французької. Членів родини, які перебувають у Канаді, можна включити в ту саму заявку. Той, хто подається поза межами Квебеку, повинен також планувати жити за його межами: провінція відбирає іммігрантів самостійно.

Конгрес українців Канади (КУК, Ukrainian Canadian Congress) привітав рішення, але вважає ліміт замалим. З 2022 року за CUAET приїхало понад 300 000 українців, і десятки тисяч із них досі мають тимчасовий статус.

Міністерство імміграції Канади опублікує посібник із подання заявки та перелік потрібних документів за два тижні до відкриття програми.

Judge: Accuracy: the source says "up to 10,000 applications starting March 2", which the post gets right. "Повного робочого стажу" is a slight distortion of "full-time work experience" (should be "рік досвіду роботи на повній ставці/повний робочий день"). The headline says "зможуть подати заявку", which is fine, but it omits the conditions and the cap. "Applicants outside Quebec must intend to live outside Quebec" is OK, but "відбирає іммігрантів самостійно" is fine. Language: "ліміт замалим" is slightly colloquial; "стаж" is a bit off for work experience in Canada; "Той, хто подається" is clumsy; "Міністерство прийме до 10 000 заявок" is OK. The glossary name "Конгрес українців Канади (КУК, Ukrainian Canadian Congress)" adds the English name, a minor deviation from the form "(КУК)". The "(PR)" abbreviation is introduced but never used again, which is padding. Usefulness: clear and complete. "Міністерство" is repeated several times and the lead is repetitive ("Міністерство прийме..." right after the IRCC mention). The post doesn't mention that the guide comes out two weeks before the opening, which gives the practical date; it does mention this, but not the date, so the reader has no concrete date for the guide.

### statcan-population

**Приріст населення Канади сповільнився до 0,2 %, а тимчасових резидентів поменшало**

У третьому кварталі населення Канади зросло на 0,2 %. Це найповільніший приріст для цього періоду від 2020 року, повідомило Статистичне управління Канади (Statistics Canada). Станом на 1 жовтня в країні налічувалося 41,7 млн людей.

Зростання майже повністю забезпечили нові постійні резиденти. Кількість тимчасових резидентів, серед яких іноземні студенти й працівники, зменшилася на 65 тисяч. Це сталося після того, як за останні два роки федеральна влада обмежила видачу дозволів на навчання й змінила програми тимчасової праці. Оттава хоче, щоб частка тимчасових резидентів у населенні була меншою.

Економісти кажуть, що повільніше зростання знизить тиск на ринок оренди у великих містах. Водночас може загостритися нестача працівників у медицині та будівництві. Найшвидше серед провінцій зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст був меншим за 0,1 %.

Judge: Accuracy: all figures, dates, provinces and the cause match the source. "Іноземні працівники" drops "temporary", but "тимчасових" appears in the same sentence, so it is a negligible slip.

Language: mostly natural. Minor problems: "від 2020 року" should be "з 2020 року". "Найповільніший приріст для цього періоду" is a slight calque of "for that period"; "найнижчий для третього кварталу" is better. "Поменшало" in the headline is colloquial. "Це сталося після того, як…" is clumsy.

Usefulness: clear and concise, with no padding. It does not say directly what this means for Ukrainians in Canada, such as newcomers on temporary status or people looking for housing or work. It stays at the level of the general news report."

### akwesasne-policing

**Поліція могавків Аквесасне й OPP підписали угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) уклали п'ятирічну угоду на 12 млн доларів. Про це рада повідомила в понеділок.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) та OPP спільно патрулюватимуть річку й шосе поблизу громади. Вона розташована на кордоні Онтаріо, Квебеку та штату Нью-Йорк. Гроші підуть також на новий відділ поліції на острові Корнвол (Cornwall Island) і на навчання восьми нових поліцейських. За словами OPP, патрулі зосередяться на боротьбі з контрабандою, а влітку — ще й на безпеці на воді.

Верховна вождиня Лора Бенедікт (Laura Benedict) наголосила, що угода визнає: першими на виклики в громаді реагують поліцейські-могавки. «Наші офіцери знають ці води й ці родини. Тепер вони матимуть ресурси для роботи», — сказала вона.

Failed checks: facts: missing: вісім\w* (нов|офіц|поліц)

Judge: Accuracy: the source is ambiguous about whether "in the summer months" modifies only boating safety or both priorities. The post resolves it as smuggling year-round and water safety in summer. This is a plausible reading but a slight interpretive narrowing. The numbers, names, the five-year term, the eight officers, the Cornwall Island station and the quote all match the source.

Language: the headline uses the bare abbreviation "OPP" before the glossary name "Провінційна поліція Онтаріо (OPP)" appears, so the first mention is not in the glossary form. "Корнвол" is an unusual rendering of Cornwall. "Вона розташована на кордоні" is slightly loose for "straddles the borders of three jurisdictions". "Відділ поліції" is acceptable, but "поліцейська дільниця" or "відділення" would be more standard. The rest reads naturally.

Usefulness: the post is clear and concise and has no padding. It does not say why this matters to Ukrainians in Canada, and it gives no context such as the border or smuggling background. It is a straightforward news summary and is adequate for the audience."

### quebec-museum

**Монреальський музей сучасного мистецтва відкривається виставкою художниці з Харкова**

У суботу після ремонту знову відкривається Монреальський музей сучасного мистецтва (Musée d'art contemporain de Montréal). Реконструкція будівлі на Place des Arts тривала чотири роки й коштувала 40 млн доларів.

Галерейна площа збільшилася на 2000 квадратних метрів. З'явилися новий вхід з вулиці Сент-Катрін (Sainte-Catherine) і безкоштовна публічна тераса. Першої неділі кожного місяця вхід до музею буде вільним.

Першою виставкою став огляд творчості художниці Катерини Лисенко (Kateryna Lysenko). Вона народилася в Харкові, а з 1998 року живе в Монреалі. На виставці представлено 60 робіт, серед них серія великих полотен, створена після її поїздки до рідного міста 2023 року. Експозиція працює до 12 квітня.

На попередньому показі в четвер Лисенко сказала, що хотіла показати Харків як місто світла, студентів і музики, а не лише як місце з новин.

Judge: Accuracy: facts match the source. Minor: "40 млн доларів" does not say Canadian dollars (the source doesn't either). "Реконструкція... коштувала" is fine. The headline says the museum "opens with the exhibition", which is fine. The "Музей... відкривається" word order in the lede is slightly awkward. Language: mostly natural. "Галерейна площа" is a slightly calqued term; "виставкова площа" would be better. "Першою виставкою став огляд" is acceptable; "Експозиція працює" is fine. "Вхід... буде вільним" is OK but "безкоштовним" is more standard. "Сент-Катрін" is acceptable (usually "Сент-Катрін"). Usefulness: clear and concise, but there is no explicit explanation of why it matters to Ukrainians in Canada beyond the Kharkiv link. It does not say the Lysenko quote is about Kharkiv's image in the context of war news. It lacks address or practical details such as the exhibition opening date being Saturday and the free admission details, though these are present.

### cra-ccb-tips

**CRA нагадала родинам подати декларацію до 30 квітня, щоб не втратити допомогу на дітей**

Агенція доходів Канади (CRA) нагадує: щоб без перерви отримувати канадську допомогу на дітей (CCB), обоє батьків мають подати податкову декларацію до 30 квітня. Це стосується й тих, хто торік не мав доходу.

Розмір допомоги щороку в липні перераховують за чистим доходом родини за попередній рік. Якщо CRA не має декларації когось із батьків, виплати зупиняють, доки її не подадуть і не опрацюють.

Новоприбулі, які ще не оформили допомогу, можуть подати заявку в кабінеті CRA My Account після отримання номера соціального страхування (SIN) або поштою на формах RC66 і RC66SCH. Друга форма містить запитання про статус резидентства та доходи за межами Канади. Нині максимальна допомога на дитину до шести років становить 8157 доларів на рік.

Безкоштовно подати декларацію можна через волонтерські податкові клініки. Вони допомагають людям зі скромним доходом.

Що можна зробити:
• Обоє батьків мають подати декларацію до 30 квітня, навіть якщо торік не мали доходу.
• Якщо ви нещодавно приїхали, подайте заявку на допомогу на дітей, щойно отримаєте SIN.
• У формі RC66SCH вказуйте всі доходи за межами Канади.
• Якщо дохід скромний, зверніться до волонтерської податкової клініки — там допоможуть безкоштовно подати декларацію.

Failed checks: form: title too long

Judge: Accuracy: the "Що можна зробити" bullet "вказуйте всі доходи за межами Канади" turns the source's description of what the form asks into advice, which is mild embellishment. The source says CRA lacks a return for "both parents", and the post says "когось із батьків", which shifts the meaning slightly. The post leaves out that payments stop in July specifically. Language: the text is mostly natural. The headline uses "CRA" and "допомогу на дітей" instead of the glossary forms on first mention, and the post says "кабінеті CRA My Account", which is a little clunky. Usefulness: the bulleted "Що можна зробити" block repeats the body almost point by point, which is padding. The post doesn't explain why the deadline matters beyond the July stop, and it never says which year's return is due.

### health-canada-recall-tips

**Maple Meadow відкликає дитячу суміш через ризик бактерії Cronobacter**

Міністерство охорони здоров'я Канади (Health Canada) закликало батьків припинити годувати дітей трьома партіями сухої дитячої суміші Maple Meadow. У продукції може бути бактерія Cronobacter. Про випадки захворювання не повідомляли.

Відкликані банки по 800 грамів продавали в продуктових магазинах і аптеках по всій країні. Термін придатності — червень 2027 року. Номери партій надруковані на дні банки.

Інфекція, яку спричиняє Cronobacter, трапляється рідко, але для немовлят вона небезпечна, особливо для недоношених і дітей зі слабким імунітетом. Її ознаки — гарячка, поганий апетит, незвичний плач і сильна млявість. Якщо після суміші в дитини з'явилися такі симптоми, одразу зверніться до лікаря або зателефонуйте на номер 811. Відкликану суміш можна повернути в магазин, де її купили, і отримати гроші назад.

Що можна зробити:
• Знайдіть на дні банки Maple Meadow номер партії та порівняйте його зі списком відкликаних партій на сайті міністерства охорони здоров'я Канади (Health Canada).
• Не годуйте дитину сумішшю з відкликаної партії. Поверніть банку в магазин, де її купили, і отримайте гроші назад.
• Якщо після суміші в дитини з'явилися гарячка, млявість, поганий апетит чи незвичний плач, одразу зверніться до лікаря або зателефонуйте на 811.
• Якщо потрібна інша суміш, порадьтеся із сімейним лікарем або педіатром.

Judge: Accuracy: "Термін придатності — червень 2027" is OK for best-before, but the "Що можна зробити" list adds things not in the source: checking the lot number against a list on the Health Canada website, and consulting a family doctor or pediatrician about alternative formula. The source mentions no such list. Also "по всій країні" is fine. "Закликало припинити годувати дітей трьома партіями" is slightly awkward, since the source says to stop using the formula. Language: "поганий апетит" for poor feeding is acceptable. "Номери партій" is fine. "Закликало... годувати трьома партіями" is an awkward construction. "Відкликає" is attributed to Maple Meadow, while the source says Health Canada recalls. Usefulness: the checklist heavily repeats the body text (return to store, symptoms, 811 appear twice), which is padding. The glossary name is used correctly on first mention, but the full name is repeated unnecessarily in the list.

