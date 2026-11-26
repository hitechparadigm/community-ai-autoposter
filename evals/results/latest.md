# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `217d6d8f` · 9/9 posts written · **4/9 passed every check** · 38 Claude calls · $0.51 ($0.057 per post)

| Check | Pass rate |
| --- | --- |
| facts | 100% |
| glossary | 100% |
| people | 100% |
| names_kept | 89% |
| language | 100% |
| form | 89% |
| reviewer | 100% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 3.89 |
| language | 3.89 |
| usefulness | 3.89 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/3/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/5 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | 4/4/4 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| quebec-museum | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | 4/4/4 |
| cra-ccb-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/3 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |

## Details

### min-wage-mb

**Мінімальна зарплата в Манітобі зросте до 16,50 долара на годину**

Нова мінімальна погодинна ставка почне діяти 1 жовтня, повідомив у вівторок уряд провінції.

Вона зросте на 65 центів. Підвищення прив'язане до інфляції в провінції — цього вимагає закон, ухвалений 2023 року. Міністр праці Манітоби Деніел Моро (Daniel Moreau) сказав на пресконференції у Вінніпезі, що мінімальну оплату отримують близько 40 тисяч людей, здебільшого в роздрібній торгівлі та сфері харчування.

Торгові палати Манітоби (Manitoba Chambers of Commerce) зазначили, що малий бізнес покриє додаткові витрати сам. Водночас організація просить у майбутньому повідомляти роботодавців про такі зміни завчасніше. За її словами, багато компаній і так платять більше за мінімальну ставку, щоб залучити працівників.

Роботодавці мають оновити оплату за всі години, відпрацьовані з 1 жовтня, зокрема для студентів і працівників з неповним навантаженням. Мінімальна ставка в Манітобі залишиться нижчою, ніж у Британській Колумбії, але вищою, ніж у Саскачевані.

Judge: Accuracy: the source's minister quote about groceries and rent is omitted (not an error). "Manitoba Chambers of Commerce" is rendered as "Торгові палати Манітоби" (plural, awkward; better "Торгово-промислова палата Манітоби"). "Employers must update pay for all hours worked from October 1" is rendered fine. "Small businesses would absorb the change" became "покриє додаткові витрати сам", which is a slight interpretive shift, and the tense is a bit off. Language: "платять більше за мінімальну ставку" is wrong; it should be "більше, ніж мінімальна ставка" or "вище за мінімальну". "Мінімальну оплату отримують близько 40 тисяч людей" is awkward; "працівників" or "отримують мінімальну зарплату" would be better. "Сфері харчування" is a calque of "food service" (better "громадське харчування"). "Сказав на пресконференції" is acceptable. "Працівників з неповним навантаженням" is slightly clumsy. The Latin-script names in parentheses are unnecessary clutter. "Мінімальна ставка залишиться нижчою, ніж..." is fine. Usefulness: clear and covers the key facts, but it omits the minister's quote on why the change matters and doesn't say what the old rate was ($15.85); the final comparison is a bit generic.

### rcmp-deepfake

**Шахраї з дипфейками виманили в мешканців Метро-Ванкувера 2,3 млн доларів**

Канадська королівська кінна поліція (RCMP) попереджає мешканців агломерації Метро-Ванкувер про любовні шахрайства, у яких аферисти видають себе за інших людей за допомогою відео, створеного штучним інтелектом.

Від початку року про втрати повідомили 85 осіб. Разом вони позбулися 2,3 млн доларів. Здебільшого зловмисники знайомилися з жертвою в застосунку для побачень або в соцмережах, а потім влаштовували короткі відеодзвінки. Під час них дипфейк підміняв обличчя та голос, і фальшива особа виглядала переконливо. Сержантка підрозділу фінансових злочинів RCMP у місті Серрі (Surrey) Прія Сандху (Priya Sandhu) зазначає: щойно з'являється довіра, шахраї починають просити гроші — на лікування, через заблокований рахунок або для вигідного вкладення.

Поліція називає тривожні ознаки: співрозмовник не може зустрітися наживо, дзвінок раптово уривається, коли його просять повернути голову, а ще він вимагає криптовалюту або подарункові картки. Якщо ви вже надіслали гроші, одразу зверніться до банку, а також повідомте місцеву поліцію та Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Judge: Accuracy: the headline says scammers "виманили" $2.3M from residents, but the source says 85 people reported losing it. That is a slight overstatement, since it covers reported losses only. "Метро-Ванкувера" is fine. "Від початку року" matches "so far this year". The body is faithful and the glossary name is used correctly. Language: mostly natural. "аферисти" and "зловмисники" are fine. "Сержантка ... зазначає: щойно з'являється довіра" is a paraphrase of the quote, which is acceptable. "вигідного вкладення" slightly softens "investment opportunity". "Вимагає" is stronger than "any request for", so "просить" would be better. "Дипфейк підміняв обличчя та голос" is a bit loose. "Любовні шахрайства" is acceptable, though "романтичні шахрайства" is also used. The English names in parentheses are unnecessary clutter. Usefulness: clear, with practical advice and no padding. The post says "Здебільшого" for "in most cases", which is correct.

### ucc-mentorship

**В Едмонтоні запустили менторську програму для новоприбулих українців**

Провінційна рада Конгресу українців Канади (КУК) в Альберті запустила в Едмонтоні менторську програму для українців, які приїхали до Канади за програмою CUAET.

Новоприбулим допомагатимуть 120 волонтерів, переважно канадські українці, які працюють у кваліфікованих робітничих професіях, медицині та інженерії. Ментор зустрічається зі своїм підопічним щонайменше двічі на місяць упродовж шести місяців. Він підказує, як шукати роботу, визнавати кваліфікацію, орендувати житло та заповнювати державні документи. Програму фінансує приватний фонд Prairie Bridges Foundation із Калгарі: за два роки він виділить 250 тисяч доларів.

«Багато людей приїхали з сильними фаховими навичками, але не знають, як тут усе працює, а пояснити їм нікому, — каже координаторка програми Галина Мороз (Halyna Moroz). — Ментор заощаджує місяці проб і помилок».

Новоприбулі й охочі стати менторами можуть подати заявки до 15 січня. Наступного року рада планує поширити програму й на Калгарі, якщо вистачить коштів.

Judge: Accuracy: mostly faithful. Minor slip: "кваліфікованих робітничих професіях" is a loose rendering of "trades" (acceptable, but slightly interpretive). "Alberta Provincial Council" is rendered as "Провінційна рада ... в Альберті", which is fine. "Сильними фаховими навичками" is OK. "Mentors... 120 volunteer mentors" is rendered as "120 волонтерів", which is fine. The post adds "Він підказує" (fine). The glossary term is used correctly: "за програмою CUAET" and "Конгрес українців Канади (КУК)". The expansion to Calgary is correct.
Language: natural overall. Small issues: "запустили/запустила" repeated in the headline and lead. "Виділить 250 тисяч доларів" omits the currency being Canadian, but the source doesn't say that either. "Заощаджує місяці проб і помилок" is slightly calque-like; "Ментор допомагає заощадити місяці..." or "позбавляє місяців проб і помилок" would be more natural. "Поширити програму й на Калгарі" is slightly awkward. "Приватний фонд ... із Калгарі" is fine. The Latin transliteration "(Halyna Moroz)" is unnecessary clutter. "Новоприбулим допомагатимуть 120 волонтерів" is fine.
Usefulness: clear, covers who, what, how, funding, deadline and expansion. It lacks mention of how to apply (no link or contact in the source). Slightly dense paragraph in the middle. The Latin name in brackets and the repeated "запустили" add small padding.

### ircc-cuaet-pr

**Для українців, які приїхали за CUAET, відкриють шлях до постійного резидентства**

Міністерство імміграції, біженців і громадянства Канади (IRCC) запускає нову програму постійного резидентства (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер.

Прийом заявок почнеться 2 березня. Міністерство прийме до 10 000 заяв. Кандидатам потрібен щонайменше рік повної зайнятості в Канаді, здобутий після приїзду за CUAET, а також результат мовного тесту не нижче CLB 5 з англійської або NCLC 5 з французької. У ту саму заяву можна включити членів родини, які перебувають у Канаді. Тим, хто живе поза Квебеком, потрібно мати намір оселитися також поза межами провінції: Квебек самостійно відбирає іммігрантів. Інструкцію до заяви й перелік потрібних документів міністерство оприлюднить за два тижні до відкриття програми.

Конгрес українців Канади (Ukrainian Canadian Congress, КУК) привітав рішення, але вважає ліміт замалим. За даними організації, з 2022 року за CUAET приїхали понад 300 000 українців, і десятки тисяч із них досі мають тимчасовий статус.

Judge: Accuracy: the 300,000 arrivals figure is attributed to the UCC ("За даними організації"), but the source states it as fact. The UCC claim applies only to the tens of thousands on temporary status. "Pathway" is rendered as "програма", which is a slight shift. Language: mostly natural. "Рік повної зайнятості" is a slightly heavy rendering of "full-time work experience". The UCC name is given as "(Ukrainian Canadian Congress, КУК)", which departs from the glossary form "Конгрес українців Канади (КУК)". "Міністерство" is repeated several times in a row. Usefulness: clear on eligibility, cap, date and the Quebec rule. The body is one dense paragraph, and it does not say what applicants should do now or what the cap means for them.

### statcan-population

**Населення Канади зросло лише на 0,2 % — найменше для третього кварталу з 2020 року**

У третьому кварталі населення Канади збільшилося на 0,2 %. Так повільно воно не зростало в цей період із 2020 року, повідомило Статистичне управління Канади (Statistics Canada). Станом на 1 жовтня в країні налічувалося 41,7 млн мешканців.

Зростання майже повністю забезпечили нові постійні резиденти. Кількість тимчасових резидентів, зокрема міжнародних студентів і тимчасових працівників-іноземців, скоротилася на 65 тисяч. Це наслідок обмежень на видачу дозволів на навчання та змін у програмах тимчасової праці, які федеральний уряд оголосив протягом двох останніх років. В Оттаві кажуть, що хочуть зменшити частку тимчасових резидентів у населенні. Серед провінцій найшвидше зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст не сягнув і 0,1 %.

Економісти вважають, що повільніше зростання послабить тиск на оренду житла у великих містах. Водночас дефіцит кадрів у медицині та будівництві може посилитися.

Failed checks: form: title too long

Judge: Accuracy: the numbers and facts match the source (0.2%, 41.7 million, October 1, 65,000, Alberta 0.5%, Ontario and BC under 0.1%). Minor slip: "the slowest pace since 2020" is rendered as "не зростало так повільно з 2020 року", which could be read as the slowest since 2020 rather than the slowest for that period since 2020. The source is itself ambiguous. The "non-permanent residents" category is rendered as "тимчасові резиденти", which is a slight simplification. "Сягнув і 0,1 %" is acceptable but changes the nuance of "less than 0.1". Language: natural and fluent. "Статистичне управління Канади (Statistics Canada)" follows the glossary. Small stylistic points: "В Оттаві кажуть" is a metonym that is fine, but "Ottawa" here means the federal government, and "У Оттаві" would be the more standard form. "Дефіцит кадрів" is fine. Usefulness: clear and concise, with no padding. The headline is repeated in the lede, which is slightly redundant. It does not explain explicitly why this matters to Ukrainians in Canada, for example for those on temporary status (CUAET), although the source does not give that either.

### akwesasne-policing

**Поліція могавків Аквесасне й OPP підписали угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) уклали п'ятирічну угоду про поліцейське обслуговування на 12 млн доларів. Про це в понеділок повідомили в раді.

Громада Аквесасне розташована на перетині кордонів Онтаріо, Квебеку та штату Нью-Йорк. Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) і OPP спільно патрулюватимуть річку та шосе поблизу громади. Частину грошей витратять на новий поліцейський відділок на острові Корнволл (Cornwall Island), ще частину — на навчання восьми нових поліцейських.

Головна вождиня Лора Бенедикт (Laura Benedict) наголосила, що угода визнає роль поліцейських-могавків: вони першими реагують на виклики в громаді. «Наші поліцейські знають ці води й ці родини. Це дає їм ресурси, щоб виконувати свою роботу», — сказала вона.

В OPP уточнили, що влітку спільні патрулі зосередяться на боротьбі з контрабандою та безпеці на воді.

Judge: Accuracy: facts largely match. Minor issues: the source says the community straddles the borders of Ontario, Quebec and New York State, and the post says "на перетині кордонів", which is acceptable. "Поліцейське обслуговування" is a slight calque of "policing agreement". The source says the money pays for a new station and training, and the post's "частину грошей... ще частину" slightly implies a split that the source doesn't state. The source says the joint patrols are "on the river and the highways", and the post keeps this. The source says "in the summer months" and the post says "влітку", which is fine. "Головна вождиня" for Grand Chief is acceptable, though "велика вождиня" is also used. The title uses the English abbreviation OPP without expanding it, while the body does expand it, which is fine. The glossary is followed on first mention in the body. The headline says "Поліція могавків Аквесасне", which is fine. Language: "уклали угоду про поліцейське обслуговування" is slightly stilted. "Реагують на виклики" adds nuance beyond "first responders", though that is acceptable. English names in parentheses are somewhat cluttered, with four of them in a short text. Usefulness: it states what happened, but doesn't say why it matters to Ukrainians in Canada, which the source doesn't provide either. The text is clear and without padding."

### quebec-museum

**Музей сучасного мистецтва в Монреалі відкривається після ремонту за 40 млн доларів**

У суботу для відвідувачів знову відчиняє двері Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal). Реконструкція будівлі на Place des Arts тривала чотири роки й коштувала 40 млн доларів.

Галерейна площа збільшилася на 2000 квадратних метрів. З'явилися новий вхід з боку вулиці Сент-Катрін і безкоштовна громадська тераса. Першої неділі кожного місяця вхід до музею вільний.

Першою виставкою стала ретроспектива Катерини Лисенко (Kateryna Lysenko). Художниця народилася в Харкові, а з 1998 року живе в Монреалі. На виставці 60 робіт, серед них серія великих полотен, які вона написала після поїздки до рідного міста 2023 року. «Я хотіла, щоб люди бачили Харків як місто світла, студентів і музики, а не лише як місце з новин», — сказала Лисенко на попередньому показі в четвер.

Виставка триватиме до 12 квітня.

Failed checks: names_kept: wrong form: Музей сучасного мистецтва Монреаля

Judge: Accuracy: "survey" rendered as "ретроспектива", which is a slight narrowing (a retrospective implies a career-spanning look back; the source says only "survey"). Other facts, numbers and dates match. Language: "галерейна площа" is a calque of "gallery space"; "виставкова площа" would be more natural. "Place des Arts" is left in Latin script without a Ukrainian form. Otherwise fluent and idiomatic. Usefulness: clear and concise, with the practical details (free first Sundays, free terrace, end date). It does not state who the audience for the Ukrainian-born artist from Kharkiv is, which is the main reason it matters to Ukrainians in Canada. It also doesn't give the museum's address or say that the post is for Montreal readers.

### cra-ccb-tips

**Без декларації до 30 квітня можна втратити допомогу на дітей**

Агенція доходів Канади (CRA) нагадує: щоб без перерви отримувати канадську допомогу на дітей (CCB), податкову декларацію мають подати обоє батьків до 30 квітня. Це потрібно навіть тим, хто торік не мав доходу. Розмір допомоги щороку в липні перераховують за чистим доходом сім'ї за попередній рік. Якщо CRA не має декларації одного з батьків, виплати зупиняють у липні й поновлюють після подання та опрацювання декларації.

Новоприбулі, які ще не оформили допомогу, можуть подати заяву через CRA My Account після отримання номера соціального страхування (SIN) або поштою. У такому разі потрібні форми RC66 і RC66SCH, де запитують про статус резидента та доходи за межами Канади.

Безплатно подати декларацію можна в громадських волонтерських податкових клініках, які допомагають людям зі скромними доходами. Максимальна допомога на дитину до шести років зараз становить 8157 доларів на рік.

Що можна зробити:
• Подайте декларацію до 30 квітня — і за себе, і за партнера, навіть якщо торік не було доходу, щоб без перерви отримувати допомогу на дітей (CCB).
• Якщо ще не оформили допомогу, зареєструйтеся в CRA My Account і подайте заяву онлайн після отримання номера соціального страхування (SIN). Можна й поштою.
• Люди зі скромними доходами можуть безплатно подати декларацію в громадських волонтерських податкових клініках.
• Якщо виплати зупинили, переконайтеся, що обоє батьків подали декларації: допомогу поновлять після їх опрацювання.

Judge: Accuracy: the source says "2026 income tax return" and the post omits the year. This is a minor omission. Also, "if CRA doesn't have a return for both parents" is rendered as "одного з батьків", which slightly shifts the meaning, though it is basically consistent. The post says "Можна й поштою" and "У такому разі потрібні форми RC66 і RC66SCH" – this is fine. The source says "families can file for free"; this is fine. "Зараз становить 8157 доларів" is fine. The headline "Без декларації ... можна втратити допомогу" is fine.
Language: mostly natural. "Новоприбулі" is okay. "Безплатно" is acceptable. "Не має декларації" is a slight calque of "doesn't have"; "не отримала" would be better. "Подайте ... за себе, і за партнера" is a slight stretch. The glossary is followed on first mention, although CCB is repeated in the bullets.
Usefulness: The "Що можна зробити" section repeats the body almost entirely, which is padding. The last bullet adds little. The post would be better without the duplication.

### health-canada-recall-tips

**Три партії дитячої суміші Maple Meadow відкликали через можливе зараження бактерією**

Міністерство охорони здоров'я Канади (Health Canada) радить батькам більше не використовувати три партії сухої дитячої суміші Maple Meadow. Вона може бути заражена бактерією Cronobacter. Про випадки захворювання поки не повідомляли.

Відкликані банки по 800 грамів продавали в продуктових магазинах і аптеках по всій Канаді. Їх позначено датою «найкраще вжити до» — червень 2027 року. Коди партій надруковані на денці банки.

Інфекція Cronobacter трапляється рідко, але для новонароджених може бути серйозною. Найбільший ризик — для дітей, які народилися передчасно або мають ослаблений імунітет. Симптоми: гарячка, погане годування, незвичний плач і сильна млявість.

Суміш не можна давати дітям. Її можна повернути до магазину, де купили, і отримати гроші назад. Якщо після такої суміші в дитини з'явилися симптоми, одразу зверніться до лікаря або зателефонуйте на номер 811.

Що можна зробити:
• Перевірте на денці банки код партії та дату «найкраще вжити до».
• Не годуйте дитину сумішшю з відкликаних партій, а банку поверніть у магазин, де її купили, — вам повернуть гроші.
• Якщо після цієї суміші в дитини з'явилися гарячка, млявість чи погане годування, одразу зверніться до лікаря або зателефонуйте на 811.
• Не знаєте, яку суміш обрати натомість, — запитайте сімейного лікаря чи фармацевта.

Judge: Accuracy: facts match the source. Minor additions: "Відкликали" in the headline is fine. The advice to ask a family doctor or pharmacist about which formula to choose is not in the source (small addition). "Вам повернуть гроші" slightly firmer than the source's "refund". Glossary: "Міністерство" is capitalized, whereas the glossary form is lowercase "міністерство охорони здоров'я Канади (Health Canada)"; this could be flagged. Language: mostly natural. "Погане годування" is a calque of "poor feeding" (better: "відмова від їжі" or "поганий апетит"). "Гарячка" is acceptable, but "підвищена температура" is more natural. "Сильна млявість" is fine. "Їх позначено датою" is a bit clumsy. "Після такої суміші" is awkward. "Не знаєте, яку суміш обрати" is a loose phrase. Usefulness: the "Що можна зробити" list repeats the body text almost verbatim (return to store, symptoms, 811, bottom of can). This is padding and repetition. The paragraph "Суміш не можна давати дітям..." also duplicates the list.

