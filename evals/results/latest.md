# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `43690943` · 9/9 posts written · **6/9 passed every check** · 44 Claude calls · $0.57 ($0.063 per post)

| Check | Pass rate |
| --- | --- |
| facts | 100% |
| glossary | 100% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 100% |
| reviewer | 89% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 4.11 |
| language | 3.89 |
| usefulness | 3.78 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 3/3/4 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| cra-ccb-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |

## Details

### min-wage-mb

**У Манітобі мінімальна зарплата зросте до 16,50 долара за годину**

Нова мінімальна ставка в Манітобі становитиме 16,50 долара за годину. Вона запрацює 1 жовтня, повідомив у вівторок уряд провінції. Підвищення — 65 центів.

Розмір ставки прив'язаний до інфляції в провінції, цього вимагає закон, ухвалений 2023 року. Міністр праці Деніел Моро (Daniel Moreau) сказав на пресконференції у Вінніпезі, що родини досі відчувають, як подорожчали продукти й оренда житла. За його словами, підвищення дає змогу зарплатам не відставати від зростання цін. Мінімальну зарплату отримують близько 40 тисяч працівників, переважно в роздрібній торгівлі та закладах харчування.

Торгова палата Манітоби (Manitoba Chambers of Commerce) заявила, що малий бізнес візьме витрати від підвищення на себе, але попросила надалі повідомляти роботодавців завчасніше. За даними палати, багато її членів і так платять більше за мінімум, щоб залучити працівників. Нова ставка вища, ніж у Саскачевані, і нижча, ніж у Британській Колумбії.

Роботодавці мають застосовувати її до всіх годин, відпрацьованих від 1 жовтня, зокрема й до роботи студентів та працівників, зайнятих неповний робочий день.

Judge: Facts all match the source. Language: "запрацює" is fine. "платять більше за мінімум" is slightly awkward (better "вище за мінімум"/"більше, ніж мінімум"). "Торгова палата Манітоби" is a loose rendering of Chambers of Commerce (better "Торгово-промислова палата"). "візьме витрати на себе" is okay. "Підвищення — 65 центів" is terse. Usefulness: clear and concise, but it doesn't say what this means for Ukrainian workers or what to do (e.g., check pay stubs), and the previous rate isn't mentioned. This isn't a problem, since the source doesn't give it.

### rcmp-deepfake

**RCMP попереджає про романтичні шахрайства з дипфейками в Метро-Ванкувері**

Канадська королівська кінна поліція (RCMP) попереджає мешканців Метро-Ванкувера про любовні шахрайства, у яких зловмисники видають себе за інших людей за допомогою відео, створеного штучним інтелектом.

Цього року про втрати повідомили 85 людей із регіону. Загалом вони втратили 2,3 млн доларів. Здебільшого шахраї знайомляться з жертвою в застосунку для побачень або в соцмережах, а потім проводять короткі відеодзвінки, де підроблені обличчя й голос допомагають створити переконливу фальшиву особу. Сержантка відділу фінансових злочинів RCMP у Серрі Прія Сандгу (Priya Sandhu) каже: «Дзвінки виглядають справжніми, саме тому ці афери такі ефективні». Коли довіра з'являється, шахрай просить гроші: нібито на лікування, через заблокований банківський рахунок або для вигідного інвестування.

Поліція називає ознаки обману: співрозмовник не може зустрітися наживо, дзвінок раптово уривається, коли його просять повернути голову, а ще він просить переказати криптовалюту або купити подарункові картки. Якщо ви вже надіслали гроші, одразу зверніться до банку, а також повідомте місцеву поліцію та Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Failed checks: reviewer: Прізвище Sandhu неправильно передано українською як «Сандгу»; має бути «Сандгу» → «Сандху».

Judge: Accuracy: the surname is rendered "Сандгу" but should be "Сандгу/Санду" (Sandhu is usually "Сандгу" or "Сандху"), so it is a questionable transliteration, and Latin spelling in brackets is padding. "Вигідного інвестування" distorts "investment opportunity" slightly. "Metro Vancouver" is inconsistent: the title has "Метро-Ванкувері" and the lead has "Метро-Ванкувера". "so far this year" is lost in "Цього року" (minor). "Він просить" refers to the partner, but the subject shifts, so it is ambiguous. Language: the title keeps "RCMP" without the glossary name, while the glossary name appears in the lead. "Любовні шахрайства" and "афери" are mixed with "романтичні". "Коли довіра з'являється" is awkward. "Каже" with the long title before the name is clumsy English-like structure. "Сержантка" is fine. "Втрати повідомили" is a calque, because people reported losses, not "reported losses" in this construction. "Для вигідного інвестування" is unnatural. Usefulness: it is clear and gives the warning signs and what to do. It lacks a separate "what to do" list, but it covers reporting. It is concise with no padding.

### ucc-mentorship

**В Едмонтоні запустили програму наставництва для українців з CUAET**

Провінційна рада Конгресу українців Канади (КУК) в Альберті запустила в Едмонтоні програму наставництва для українців, які приїхали до Канади за програмою CUAET. Новоприбулим допомагатимуть 120 волонтерів-наставників.

Більшість із них — канадські українці, які працюють у кваліфікованих робітничих професіях, медицині та інженерії. Наставник зустрічається зі своїм підопічним щонайменше двічі на місяць упродовж шести місяців. Він допомагає шукати роботу, підтверджувати кваліфікацію, орендувати житло й заповнювати урядові форми. Програму фінансує Prairie Bridges Foundation, приватний фонд із Калгарі: він виділив на два роки 250 тисяч доларів.

Координаторка програми Галина Мороз (Halyna Moroz) пояснює: «Багато хто приїхав із міцними навичками, але не знає, як тут усе працює, і ніхто їм цього не пояснює. Наставник економить місяці спроб і помилок».

Заявки від новоприбулих і від охочих стати наставниками приймають до 15 січня. Наступного року рада планує поширити програму на Калгарі, якщо вистачить коштів.

Judge: Facts (120 mentors, twice a month for six months, $250,000 over two years, 15 January, Calgary expansion) match the source. Glossary: the headline is the first mention and uses "з CUAET" instead of "програма CUAET". Language: "урядові форми" is a calque of "government forms", and "державні форми/документи" would be more natural. "Кваліфікованих робітничих професіях" is a bit stiff for "trades". The Prairie Bridges sentence is crammed into the mentor-duties paragraph. The post says nothing on how to apply, but the source gives no details either. The dollars are not specified as Canadian, which matches the source.

### ircc-cuaet-pr

**Для українців із CUAET відкриють шлях до постійного резидентства**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє новий шлях до постійного резидентства (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер.

Подати заяву можна буде з 2 березня, а прийматимуть до 10 000 заяв. Потрібно щонайменше рік пропрацювати в Канаді на повну ставку після приїзду за CUAET. Також необхідний результат мовного тесту не нижче CLB 5 з англійської або NCLC 5 з французької. Членів родини, які перебувають у Канаді, можна вказати в тій самій заяві. Заявники, які перебувають поза Квебеком, мусять також мати намір жити поза Квебеком: ця провінція сама відбирає іммігрантів. Посібник для заявників і перелік потрібних документів міністерство імміграції Канади оприлюднить за два тижні до відкриття.

Конгрес українців Канади (КУК) привітав рішення, але вважає ліміт замалим. З 2022 року за CUAET приїхали понад 300 000 українців, і, за даними КУК, десятки тисяч із них досі мають тимчасовий статус.

Judge: Accuracy: all facts, numbers, dates and glossary names match the source. Language: "мусять" is slightly colloquial and "повинні" would be better. "ліміт замалим" is a bit informal. The main paragraph is dense and could be split into shorter ones. Usefulness: clear and complete, but the eligibility details are packed into one block, which makes them harder to scan.

### statcan-population

**Населення Канади зросло найповільніше для третього кварталу з 2020 року**

У третьому кварталі населення Канади збільшилося лише на 0,2 %. Це найнижчий приріст для цього періоду з 2020 року, повідомило Статистичне управління Канади (Statistics Canada). Станом на 1 жовтня в країні проживало 41,7 млн людей.

Зростання майже повністю забезпечили нові постійні резиденти. Кількість непостійних резидентів, до яких належать іноземні студенти й тимчасові працівники, скоротилася на 65 тисяч. Це наслідок обмежень на видачу дозволів на навчання та змін у програмах тимчасової праці, які федеральний уряд оголосив упродовж двох останніх років. В Оттаві кажуть, що хочуть зменшити частку тимчасових резидентів у населенні.

Серед провінцій найшвидше зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст був нижчим за 0,1 %. Економісти вважають, що повільніше зростання послабить тиск на оренду житла у великих містах, але може загострити нестачу працівників у медицині та будівництві.

Judge: Accuracy: "Ottawa has said" rendered as "В Оттаві кажуть", ambiguous (federal government is meant), minor. "Лише" in the lead adds slight editorializing. Headline "найповільніше для третього кварталу" is awkward/calque-like; better "найповільніше за третій квартал з 2020 року". "іноземні студенти" vs "international students" is OK; "нові постійні резиденти" fine. "В Онтаріо" should be "В Онтаріо"/"В Онтарио" fine; "нижчим за 0,1 %" is correct. Glossary: Statistics Canada term used correctly. Usefulness: neutral news summary with no explicit relevance for Ukrainians in Canada (e.g., newcomers, students, workers, permits); no "what to do" or audience angle; "постійні резиденти" not glossed as PR terms (glossary terms for PR not required here). Also "tillki" source says "Wednesday" omitted — fine.

### akwesasne-policing

**Поліція могавків і OPP підписали угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) підписали п'ятирічну угоду про поліцейське обслуговування вартістю 12 млн доларів. Про це рада повідомила в понеділок.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) і OPP спільно патрулюватимуть річку та шосе поблизу громади. Вона розташована на межі Онтаріо, Квебеку та штату Нью-Йорк. Гроші підуть також на новий відділок на острові Корнволл (Cornwall Island) і на навчання восьми нових поліцейських. За словами OPP, влітку патрулі зосередяться на боротьбі з контрабандою та на безпеці на воді.

Головна вождиня Лора Бенедикт (Laura Benedict) зазначила, що угода визнає поліцейських-могавків тими, хто першим реагує на події в громаді. «Наші поліцейські знають ці води й ці родини. Тепер вони матимуть ресурси для роботи», — сказала вона.

Judge: Accuracy: the source says the OPP joint patrols would focus on smuggling and boating safety, and the post attributes this correctly. Minor issues: "Grand Chief" is rendered as "Головна вождиня", which is acceptable, though "Верховна вождиня" is a common alternative. The post turns "the council said Monday" into "Про це рада повідомила в понеділок", which is fine. "Which straddles the borders" is simplified to "на межі", and the sentence "Вона розташована" is ambiguous because "вона" could refer to the river or the community. The post also drops that the community straddles Ontario, Quebec and New York, which is fine. Language: the wording is mostly natural. "Поліція могавків" in the headline is slightly loose, since "Поліцейська служба могавків Аквесасне" is the proper name. "Мохок-ради" is not used, and the glossary term is used correctly. "Тими, хто першим реагує на події" is slightly awkward; "перші, хто реагує" or "першими на місці події" would be better. Usefulness: it reports the news clearly but gives no explanation of why it matters to Ukrainians in Canada, and has no context. The headline mixes the abbreviation OPP with a Ukrainian name without expanding it, which is acceptable under the glossary.

### quebec-museum

**Музей сучасного мистецтва Монреаля відкривається після ремонту за 40 млн доларів**

У суботу для відвідувачів знову відчиняє двері Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal). Будівлю на Place des Arts ремонтували чотири роки, а робота коштувала 40 млн доларів.

Тепер у музею на 2000 квадратних метрів більше виставкових залів, є новий вхід з боку вулиці Сент-Катрін і безкоштовна публічна тераса. Першої неділі кожного місяця вхід буде вільний.

Відкриває оновлений музей виставка художниці Катерини Лисенко (Kateryna Lysenko). Вона народилася в Харкові, а з 1998 року живе в Монреалі. На виставці 60 робіт, зокрема серія великих полотен, які Лисенко створила після поїздки до рідного міста 2023 року.

«Я хотіла, щоб люди побачили Харків як місто світла, студентів і музики, а не лише як місце з новин», — сказала художниця на презентації в четвер. Виставка триватиме до 12 квітня.

Judge: Accuracy: all numbers, dates and names match. Minor slip: "preview" became "презентація", which suggests a presentation, not a preview (прев'ю / попередній перегляд). The "survey" nature of the show (a retrospective) is lost; "виставка художниці" is vaguer. Language: "а робота коштувала 40 млн" is awkward, because "ремонт коштував" would be more natural. "вхід буде вільний" is acceptable but "безкоштовний" is more usual. "Тепер у музею" is slightly clunky. Otherwise fluent. Usefulness: clear and concise, and the Kharkiv-born artist gives a Ukrainian link. It has no practical details such as address, hours or ticket prices, and it does not spell out why the story matters to Ukrainians in Canada.

### cra-ccb-tips

**Без податкової декларації допомога на дітей припиниться з липня**

Агенція доходів Канади (CRA) нагадує: щоб без перебоїв отримувати канадську допомогу на дітей (CCB), декларацію за 2026 рік потрібно подати до 30 квітня. Це стосується й тих, хто торік не мав доходу.

Розмір допомоги щороку в липні перераховують за чистим доходом сім'ї за попередній рік. Якщо в агенції немає декларації когось із батьків, виплати зупиняються в липні й відновлюються після того, як декларацію подадуть і опрацюють. Максимальна допомога на дитину до шести років тепер становить 8157 доларів на рік.

Що можна зробити:
• Домовтеся з партнером і подайте обидві декларації до 30 квітня, навіть якщо торік дохід був нульовий.
• Якщо ви ще не оформили CCB, подайте заяву в CRA My Account після отримання номера соціального страхування (SIN).
• Надсилаєте заяву поштою? Заповніть форми RC66 і RC66SCH, де питають про статус проживання та доходи за межами Канади.
• Якщо дохід невисокий, подайте декларацію безкоштовно через громадські волонтерські податкові клініки.

Judge: Accuracy: the source says payments stop "if the CRA does not have a return for both parents"; the post says "когось із батьків" (either parent), which is acceptable. The headline "Без податкової декларації допомога припиниться з липня" is slightly oversimplified, but fine. "Максимальна допомога на дитину до шести років ... 8157 доларів на рік" is correct. Source oddity: it calls it the "2026 income tax return" filed by April 30 for "last year", and the post repeats this faithfully. Language: "Агенція доходів Канади" matches the glossary. "допомога на дітей" and then "допомога на дитину" is fine. "Розмір допомоги ... перераховують за чистим доходом" is a little clumsy; "на підставі" would be better. "заяву в CRA My Account" is slightly awkward; "через" would be better. "Надсилаєте заяву поштою?" is OK. "Подайте декларацію безкоштовно" is fine. Usefulness: clear and practical. The what-to-do list repeats the body (the 30 April deadline, July). "Домовтеся з партнером" is mild invented advice but safe. The post omits that the clinics are for people with modest incomes, though "Якщо дохід невисокий" covers it. The post says payments resume after the return is processed; the source implies this, so it is fine.

### health-canada-recall-tips

**У Канаді відкликали три партії дитячої суміші Maple Meadow**

Міністерство охорони здоров'я Канади (Health Canada) закликає батьків припинити використання трьох партій сухої дитячої суміші Maple Meadow. Вона може бути заражена бактерією Cronobacter. Йдеться про банки по 800 грамів, термін придатності яких спливає в червні 2027 року. Номери партій надруковані на денці кожної банки. Суміш продавали в продуктових магазинах і аптеках по всій країні. Про випадки захворювання не повідомляли.

Інфекція Cronobacter трапляється рідко, але для новонароджених може бути небезпечною. Найбільший ризик — для недоношених дітей і малюків з ослабленим імунітетом. Ознаки: гарячка, поганий апетит, незвичний плач і сильна млявість.

Годувати дітей відкликаною сумішшю не можна. Її варто повернути в магазин, де купили, і отримати гроші назад. Якщо після такої суміші в дитини з'явилися симптоми, треба негайно звернутися до лікаря або зателефонувати на 811.

Що можна зробити:
• Знайдіть удома банки Maple Meadow по 800 г і зіставте номер партії на денці з номерами в повідомленні Health Canada.
• Банки із зазначених партій відкладіть окремо, щоб ніхто не використав їх для годування.
• Перед поверненням сфотографуйте номер партії та збережіть чек, якщо він є: так легше отримати гроші назад.
• Якщо дитина вже пила цю суміш, стежте за її станом і за перших ознак хвороби телефонуйте лікарю або на 811.

Judge: Accuracy: "термін придатності спливає в червні 2027" is OK for best-before. "Про випадки захворювання не повідомляли" is fine. The post says "порівняйте з номерами в повідомленні Health Canada", but the source gives no lot numbers, so the audience can't compare without a link; this is a minor gap. The phrase "після такої суміші" is slightly loose. The advice to photograph the lot number and keep the receipt is general and safe, though "чек, якщо він є" is an addition. Language: the glossary name is used correctly, but "Міністерство" is capitalized while the glossary has lowercase. "Поганий апетит" is a weak rendering of "poor feeding", and "гроші назад" is a bit colloquial. Some repetition: the symptoms and the 811 call appear twice, in the body and in the list. The post doesn't mention that 811 is a Canadian health line. The "Що можна зробити" list is mostly sound.

