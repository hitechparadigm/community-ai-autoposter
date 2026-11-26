# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `217d6d8f` · 9/9 posts written · **5/9 passed every check** · 40 Claude calls · $0.56 ($0.062 per post)

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
| accuracy | 3.78 |
| language | 4.00 |
| usefulness | 3.67 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |
| akwesasne-policing | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| cra-ccb-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | 3/4/3 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/3 |

## Details

### min-wage-mb

**У Манітобі мінімальна зарплата зросте до 16,50 долара на годину**

З 1 жовтня мінімальна оплата праці в Манітобі становитиме 16,50 долара за годину. Уряд провінції оголосив про це у вівторок. Ставка зросте на 65 центів.

Підвищення прив'язане до рівня інфляції в провінції, як вимагає закон, ухвалений 2023 року. Міністр праці Манітоби Деніел Моро (Daniel Moreau) повідомив, що мінімальну зарплату отримують близько 40 000 працівників, здебільшого в роздрібній торгівлі та громадському харчуванні. За його словами, родини й досі відчувають подорожчання продуктів та оренди, а підвищення допомагає зарплатам не відставати від цін.

Торгова палата Манітоби (Manitoba Chambers of Commerce) зазначила, що малий бізнес покриє ці витрати, але попросила владу в майбутньому повідомляти роботодавців про такі зміни заздалегідь. За даними палати, багато її членів і так платять більше за мінімум, щоб залучити працівників.

Ставка в Манітобі залишиться нижчою, ніж у Британській Колумбії, і вищою, ніж у Саскачевані. Роботодавці мають платити за новою ставкою за всі відпрацьовані години, зокрема студентам і працівникам із неповним робочим днем.

Judge: Accuracy: mostly faithful. "Employers must update pay for all hours worked from October 1" is rendered as "pay at the new rate for all hours worked", which is acceptable. "Small businesses would absorb the change" became "покриє ці витрати", which is a slight shift but fine. The original says Moreau spoke at a news conference in Winnipeg; this is omitted, which is minor. The "Tuesday" detail is kept. Language: generally natural. "платять більше за мінімум" is slightly awkward; "понад мінімум" or "більше за мінімальну" would be better. "Мінімальна оплата праці" and "мінімальна зарплата" are used interchangeably, which is fine. "Громадське харчування" is correct. "Працівникам із неповним робочим днем" is a bit clunky; "тим, хто працює неповний день" is better. The English names in brackets are acceptable but cluttered. "Ставка зросте на 65 центів" is OK. Usefulness: clear and complete. The second paragraph is dense, and the post lacks a note on the previous rate ($15.85), which is not in the source anyway.

### rcmp-deepfake

**RCMP попереджає про романтичні шахрайства з дипфейками у Великому Ванкувері**

Канадська королівська кінна поліція (RCMP) попереджає мешканців Великого Ванкувера (Metro Vancouver) про шахраїв, які видають себе за інших людей у відеодзвінках. Обличчя і голос у таких розмовах підроблені за допомогою штучного інтелекту.

Цього року 85 людей повідомили, що загалом втратили 2,3 млн доларів. У більшості випадків шахрай знайомився з жертвою в застосунку для знайомств або в соцмережах, а потім проводив короткі відеодзвінки. Коли жертва починала довіряти, шахрай просив грошей: нібито на лікування, через заблокований рахунок або для вигідних інвестицій. «Дзвінки виглядають справжніми, і саме тому ці схеми такі ефективні», — сказала сержантка відділу фінансових злочинів RCMP у місті Суррей (Surrey) Прія Сандху (Priya Sandhu).

Поліція називає такі ознаки: співрозмовник не може зустрітися наживо, дзвінок раптово уривається, коли його просять повернути голову, він просить гроші в криптовалюті або подарункових картках. Тим, хто вже переказав кошти, слід негайно звернутися до банку, а також повідомити місцеву поліцію і Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Judge: Accuracy: numbers, names and the quote match the source. Minor slips: "medical emergency" became "на лікування" (treatment), which is narrower, and "investment opportunity" became "вигідних інвестицій" (profitable investments), which adds an evaluative word. The headline uses bare "RCMP" instead of the glossary form on first mention. Language: mostly natural. "Романтичні шахрайства" is a calque of "romance scams"; "шахрайства в стосунках" or "любовні шахрайства" would read better. "Видають себе за інших людей" is slightly vague. The warning-signs sentence is a run-on with an unclear subject ("він"). Usefulness: clear and practical, with warning signs and what to do. It has no local angle for Ukrainian readers and no mention of the dating-app context in the lead.

### ucc-mentorship

**В Едмонтоні запустили менторську програму для новоприбулих українців**

Альбертська провінційна рада Конгресу українців Канади (КУК) запустила в Едмонтоні менторську програму для українців, які приїхали до Канади за програмою CUAET.

Новоприбулим допомагатимуть 120 волонтерів-менторів. Здебільшого це українці Канади, які працюють у робітничих професіях, медицині та інженерії. Ментор зустрічається зі своїм підопічним щонайменше двічі на місяць упродовж шести місяців. Він допомагає шукати роботу, підтверджувати кваліфікацію, орендувати житло й заповнювати державні документи. Програму фінансує приватний фонд Prairie Bridges Foundation з Калгарі: він зобов'язався виділити 250 тисяч доларів протягом двох років.

Координаторка програми Галина Мороз (Halyna Moroz) каже, що багато людей приїхали з сильним фахом, але не знають, як тут усе працює, а пояснити їм нікому. Ментор, за її словами, економить місяці спроб і помилок. Заявки від новоприбулих і від охочих стати менторами приймають до 15 січня. Якщо вистачить коштів, наступного року програму розширять на Калгарі.

Judge: Accuracy: facts match (120 mentors, twice a month, six months, $250,000 over two years, Jan 15, Calgary expansion). Minor slip: "робітничих професіях" is a loose rendering of "trades" (better "кваліфікованих робітничих фахах"/"ремеслах"). The post says "Новоприбулим допомагатимуть 120 волонтерів", which is fine. "Prairie Bridges Foundation" left in Latin without Ukrainian rendering, acceptable. Program name "Альбертська провінційна рада" is a bit clunky (more natural "Провінційна рада Альберти"). Language: mostly natural; "Ментор ... економить місяці спроб і помилок" is an indirect paraphrase of the quote, fine. "Галина Мороз (Halyna Moroz)" Latin transliteration in brackets is unnecessary. "приватний фонд ... з Калгарі: він зобов'язався" is OK. Glossary terms used correctly. Usefulness: informative and has deadline, but the first-paragraph and the program details are dense; the key practical info (how to apply/where, who is eligible as a mentor) is missing in the source; the final paragraph merges the quote with the deadline and expansion, which makes the structure slightly muddled. The funding sentence is buried in the paragraph about mentor duties.

### ircc-cuaet-pr

**Для українців із CUAET відкриють шлях до постійного резидентства**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє нову програму постійного резидентства (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер.

Заявки почнуть приймати 2 березня, усього прийматимуть до 10 000 заяв. Кандидатам потрібен щонайменше рік роботи на повну ставку в Канаді, здобутий після приїзду за CUAET, а також результат мовного тесту не нижче CLB 5 з англійської або NCLC 5 з французької. Членів родини, які перебувають у Канаді, можна вказати в тій самій заяві. Заявники, які живуть поза Квебеком, мають і надалі планувати жити поза ним: ця провінція сама відбирає іммігрантів.

Конгрес українців Канади (КУК) привітав рішення, але вважає ліміт замалим. З 2022 року за CUAET приїхали понад 300 000 українців, і, за даними КУК, десятки тисяч із них досі мають тимчасовий статус.

Міністерство імміграції Канади оприлюднить посібник із подання заявки та перелік потрібних документів за два тижні до відкриття програми.

Judge: Accuracy: "Applicants outside Quebec must also intend to live outside Quebec" is rendered fine, but "мають і надалі планувати жити поза ним" slightly alters meaning ("continue to plan"). Headline says "відкриють шлях" without noting it is a limited pathway (10,000 cap) or the date. "Усього прийматимуть до 10 000 заяв" is fine. "Нову програму" for "pathway" is a slight shift (pathway ≠ program), and "who live outside Quebec" vs source "who are outside Quebec" is a minor shift. Language: comma splice "2 березня, усього прийматимуть" is clumsy; "здобутий після приїзду за CUAET" is slightly awkward; "посібник із подання заявки" OK. "Заявки" and "заяв" repeated. Glossary followed, but the last paragraph repeats the full ministry name instead of the short form "IRCC"/"міністерство імміграції Канади", which is allowed. Usefulness: clear and complete, but lacks practical takeaway beyond the facts (e.g. what to do now: guide to be published two weeks before opening, i.e. about Feb 16). The "two weeks before" is not converted to a date, and the "Thursday" is ambiguous. Minor repetition of the ministry mention.

### statcan-population

**Населення Канади зросло лише на 0,2 % — найповільніше з 2020 року**

За третій квартал населення Канади збільшилося на 0,2 %. Це найповільніший приріст за цей період з 2020 року, повідомило Статистичне управління Канади (Statistics Canada). На 1 жовтня в країні було 41,7 млн людей.

Зростання майже повністю забезпечили нові постійні резиденти. Кількість непостійних резидентів, до яких належать іноземні студенти й тимчасові працівники, скоротилася на 65 тисяч. Скорочення сталося після обмежень на видачу дозволів на навчання та змін у програмах тимчасової праці, ухвалених за останні два роки. Федеральний уряд хоче, щоб частка тимчасових резидентів у населенні зменшилася.

Серед провінцій найшвидше зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст був нижчим за 0,1 %. Економісти кажуть, що повільніше зростання може послабити тиск на оренду житла у великих містах, але може посилити брак працівників у медицині та будівництві.

Judge: Accuracy: headline drops "for that period" (source says the slowest Q3 pace since 2020), so it reads as slowest overall since 2020. "Temporary foreign workers" is shortened to "тимчасові працівники", which loses "foreign". Language: "тиск на оренду житла" is a slightly calqued phrase (better "тиск на ринок оренди"). "Скоротилася… Скорочення сталося" repeats the same word. "У медицині" is a loose rendering of health care (better "охорона здоров'я"). Usefulness: the post reports the facts but does not say what this means for Ukrainians in Canada, for example for newcomers on temporary status, study permits or work permits, or for the path to PR. It also adds no context beyond the source.

### akwesasne-policing

**Поліція могавків і OPP підписали п'ятирічну угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) уклали п'ятирічну угоду про поліцейське обслуговування на 12 млн доларів. Про це в понеділок повідомила рада.

За угодою Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) та OPP спільно патрулюватимуть річку й автотраси поблизу громади. Вона розташована на перетині кордонів Онтаріо, Квебеку та штату Нью-Йорк. Кошти підуть також на нове відділення поліції на острові Корнуолл (Cornwall Island) і на навчання восьми нових поліцейських.

Головна вождиня ради Лора Бенедікт (Laura Benedict) наголосила, що угода визнає: саме поліцейські-могавки першими реагують на виклики в громаді. «Наші офіцери знають ці води й ці родини. Тепер у них є ресурси, щоб робити свою справу», — сказала вона. За словами OPP, влітку спільні патрулі зосередяться на боротьбі з контрабандою та безпеці на воді.

Failed checks: facts: missing: (вісім|вісьм)\w* (нов|офіц|поліц)

Judge: Accuracy: the facts match overall. Minor slip: "Mohawk Council of Akwesasne" is rendered as "Рада могавків Аквесасне", which is acceptable. "Grand Chief" is rendered as "Головна вождиня", which is fine. The statement "влітку... на боротьбі з контрабандою" is faithful. "Поліцейські-могавки" for "Mohawk police" is a fair rendering. The source says the community straddles the borders, and "розташована на перетині кордонів" is fine. "Resources to do the job" is fine. The source says "Monday" and the post does too. The headline uses "OPP" without the Ukrainian name, but the glossary name appears in the body on first mention, as required. Calling the Akwesasne police "Поліцейська служба могавків Аквесасне" is okay. Language: mostly natural. "Уклали угоду про поліцейське обслуговування" is a bit bureaucratic. "Автотраси" is slightly odd, and "траси" or "шосе" would be more natural. "Офіцери" for officers is a slight calque, and "поліцейські" would be better. "Зосередяться на боротьбі з контрабандою та безпеці на воді" is slightly awkward because the verbs and nouns don't pair well. The English names in parentheses are heavy for a short text. Usefulness: it clearly says what happened. It doesn't explain why it matters to Ukrainians in Canada, but the source gives little to work with. The sentence "Вона розташована..." has an unclear antecedent: it could refer to the service or the community, and "громади" is only the nearest noun. The headline abbreviates to "OPP" in Latin script without explanation, which is slightly unclear to readers.

### quebec-museum

**Монреальський музей сучасного мистецтва відкривається після реконструкції**

У суботу для відвідувачів знову відчиняє двері Музей сучасного мистецтва в Монреалі (Musée d'art contemporain de Montréal). Реконструкція його будівлі на Place des Arts тривала чотири роки й коштувала 40 млн доларів.

Площа галерей збільшилася на 2 000 квадратних метрів. Тепер у музею є новий вхід з боку вулиці Сент-Катрин і безкоштовна громадська тераса. Щопершої неділі місяця вхід буде вільним.

Першою виставкою стала ретроспектива художниці Катерини Лисенко (Kateryna Lysenko), яка народилася в Харкові та з 1998 року живе в Монреалі. Тут показують 60 робіт, зокрема серію великих полотен, написаних після її поїздки до рідного міста в 2023 році. «Я хотіла, щоб люди бачили Харків як місто світла, студентів і музики, а не лише як місце з новин», — сказала Лисенко на презентації в четвер.

Виставка триває до 12 квітня.

Judge: Accuracy: "ретроспектива" for "survey" is a slight stretch (survey is not necessarily a retrospective); "Тут показують 60 робіт" is fine. "на презентації" for "preview" is slightly off (прев'ю / попередній показ for press/preview). "Вхід буде вільним" okay. Source does not say "currently" or "opening exhibition" issues—fine. Language: mostly natural; "Першою виставкою стала" is OK but "Відкриває музей виставка" better; "відчиняє двері" fine; mixing Place des Arts in Latin script untranslated (could be "Палац мистецтв"/"Пляс-де-Ар"); "Сент-Катрин" ok (usually "Сент-Катрін"). "Реконструкція ... коштувала 40 млн доларів" - currency not specified as CAD; the source says $40-million, so fine. Usefulness: clear and complete, but lacks Ukrainian angle emphasis (Kharkiv framing is present); no practical details like address or ticket prices, no explicit why-it-matters link for Ukrainians in Canada beyond the Kharkiv-born artist.

### cra-ccb-tips

**Родини мають подати декларацію до 30 квітня, щоб не втратити допомогу на дітей**

Агенція доходів Канади (CRA) нагадала: щоб без перерви отримувати канадську допомогу на дітей (CCB), потрібно подати податкову декларацію до 30 квітня. Це стосується й тих, хто торік не мав доходу. Розмір допомоги щороку в липні переглядають за чистим доходом родини за попередній рік. Якщо в агенції немає декларації когось із батьків, виплати зупиняють у липні, доки документ не подадуть і не опрацюють.

Новоприбулі, які ще не оформили допомогу, можуть зробити це через особистий кабінет CRA My Account після отримання номера соціального страхування (SIN) або поштою — за формами RC66 і RC66SCH. У другій формі потрібно вказати статус резидентства та доходи за межами Канади.

Безкоштовно подати декларацію допоможуть волонтерські податкові клініки у громадах. Вони працюють для людей зі скромним доходом. Максимальна допомога на дитину до шести років тепер становить 8157 доларів на рік.

Що можна зробити:
• Обоє з батьків мають подати декларацію до 30 квітня, навіть якщо торік не мали доходу.
• Новоприбулі можуть оформити канадську допомогу на дітей (CCB) після отримання SIN — в особистому кабінеті Агенції доходів Канади (CRA) або поштою.
• Людям зі скромним доходом безкоштовно допоможуть заповнити декларацію у волонтерській податковій клініці.
• Перевіряйте в CRA My Account, чи опрацювали декларацію і чи надходять виплати.

Failed checks: form: title too long

Judge: Accuracy: the last bullet ("check in CRA My Account whether the return was processed and payments are arriving") is advice not in the source, so it is invented. The "2026" tax year is dropped, but this is minor. The headline uses "допомогу на дітей" instead of the glossary form on first mention. Language: mostly natural. The glossary names are repeated in the bullets: "канадську допомогу на дітей (CCB)" and "Агенція доходів Канади (CRA)" are re-expanded, which is clumsy. "Допомога на дітей" and "допомога на дитину" are mixed. Usefulness: the "Що можна зробити" list repeats the body almost word for word, which is padding. The list also contains the unsupported tip. The key facts are clear: the April 30 deadline, the July stop of payments, the newcomer application route, free clinics and the maximum amount.

### health-canada-recall-tips

**Три партії дитячої суміші Maple Meadow відкликали через ймовірне зараження бактерією**

Міністерство охорони здоров'я Канади (Health Canada) радить батькам припинити користуватися трьома партіями сухої дитячої суміші Maple Meadow. Вона може бути заражена бактерією Cronobacter. Відкликали банки по 800 грамів із терміном придатності до червня 2027 року. Їх продавали в продуктових крамницях і аптеках по всій країні. Коди партій надруковані на денці кожної банки. Про випадки захворювання не повідомляли.

Інфекція Cronobacter трапляється рідко, але може бути небезпечною для новонароджених, особливо для недоношених дітей і малюків зі слабкою імунною системою. Вона проявляється гарячкою, поганим апетитом, незвичним плачем і сильною млявістю. Якщо після суміші в дитини з'явилися такі симптоми, одразу телефонуйте лікареві або на номер 811.

Відкликану суміш не можна давати дитині. Її слід повернути до крамниці, де купували, і отримати гроші назад.

Що можна зробити:
• Перегляньте на денці банки код партії й термін придатності та порівняйте їх зі списком відкликаних партій на сайті міністерства охорони здоров'я Канади (Health Canada).
• Не давайте відкликану суміш дитині й нікому не віддавайте. Поверніть банку до крамниці, де купували, і отримайте гроші назад.
• Якщо після суміші в дитини з'явилися гарячка, млявість, поганий апетит чи незвичний плач, одразу телефонуйте лікареві або на номер 811.
• Якщо потрібна інша суміш, порадьтеся з сімейним лікарем або педіатром. Не готуйте суміш самостійно й не змінюйте пропорцій розведення.

Judge: Accuracy: "best-before dates in June 2027" is rendered as "термін придатності до червня 2027" (best-before is not the same as expiry, and "до червня" can mean "before June"). The post says to compare codes with "a list of recalled lots on the Health Canada website", but the source never mentions a website or list. The source also doesn't say to avoid giving the formula to anyone else, or to talk to a doctor or pediatrician about alternative formula, or not to prepare formula yourself or change dilution. These are invented advice. "Sold across Canada" is rendered correctly. Language: mostly natural. "Телефонуйте лікареві" is a bit awkward, and "на денці" and "проявляється" are acceptable. The glossary name is used correctly at first mention, but the full name is repeated unnecessarily in the bullets. Usefulness: the "Що можна зробити" list repeats the body text almost verbatim (return to store, symptoms, 811), which is padding. Part of the list is invented advice. The headline is vague about the specific bacterium (Cronobacter is named only in the body) and omits the no-illnesses detail until the end.

