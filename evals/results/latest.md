# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `9e1711fd` · 9/9 posts written · **5/9 passed every check** · 46 Claude calls · $0.62 ($0.068 per post)

| Check | Pass rate |
| --- | --- |
| facts | 89% |
| glossary | 89% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 89% |
| reviewer | 89% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 4.11 |
| language | 4.00 |
| usefulness | 3.89 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/5/4 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/3/4 |
| cra-ccb-tips | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/4 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | 4/4/4 |

## Details

### min-wage-mb

**У Манітобі з 1 жовтня мінімальна зарплата зросте до 16,50 долара**

Уряд Манітоби у вівторок оголосив, що з 1 жовтня мінімальна оплата праці в провінції становитиме 16,50 долара за годину. Підвищення — на 65 центів. Його прив'язано до рівня інфляції в провінції, як вимагає закон, ухвалений 2023 року.

Мінімальну зарплату отримують близько 40 тисяч працівників, здебільшого в роздрібній торгівлі та сфері харчових послуг. Міністр праці Манітоби Даніель Моро (Daniel Moreau) пояснив рішення тим, що родини досі відчувають високі ціни на продукти й оренду житла. Нову ставку роботодавці мають застосовувати до всіх відпрацьованих годин від 1 жовтня, зокрема для студентів і працівників на неповну ставку. Мінімальна оплата праці в Манітобі залишатиметься нижчою, ніж у Британській Колумбії, але вищою, ніж у Саскачевані.

Торгова палата Манітоби (Manitoba Chambers of Commerce) зазначила, що малий бізнес візьме додаткові витрати на себе, але попросила в наступні роки повідомляти про такі зміни раніше. Багато її членів і так платять більше за мінімальну ставку, щоб залучити працівників.

Judge: Facts match the source: date, amount, 65 cents, 2023 law, 40,000 workers, comparisons with BC and Saskatchewan, and the Chamber of Commerce position. Language problems: "платять більше за мінімальну ставку" should be "платять більше, ніж мінімальна ставка" (wrong government). "Візьме додаткові витрати на себе" is slightly awkward, and "Даніель Моро" with the English name in brackets is acceptable. "Мінімальна оплата праці" and "мінімальна зарплата" are used interchangeably, which is fine. Usefulness: clear and concise, but it has no practical takeaway for workers or employers, such as checking that pay stubs reflect the new rate. The Moreau quote is paraphrased rather than quoted, which is fine. The headline says "до 16,50 долара", which is correct.

### rcmp-deepfake

**RCMP попереджає про любовні шахрайства з дипфейками в Метро-Ванкувері**

Канадська королівська кінна поліція (RCMP) застерігає мешканців Метро-Ванкувера про любовні шахрайства, у яких зловмисники видають себе за реальних людей. Для цього вони використовують відео, створене штучним інтелектом.

Від початку року про втрати повідомили 85 мешканців регіону. Загалом вони втратили 2,3 млн доларів. У більшості випадків шахрай знайомився з жертвою в застосунку для знайомств або в соцмережах, а потім проводив короткі відеодзвінки. Підроблені обличчя й голос (дипфейк) робили вигадану особу переконливою.

«Дзвінки виглядають справжніми, тому ці схеми такі ефективні», — каже сержантка відділу фінансових злочинів RCMP в місті Суррей (Surrey) Прія Сандху (Priya Sandhu). За її словами, коли довіра виникає, починаються прохання про гроші: нібито на лікування, через заблокований банківський рахунок або для вигідних інвестицій.

Поліція називає ознаки обману: співрозмовник не може зустрітися наживо, а дзвінок раптово уривається, коли його просять повернути голову. Насторожити має і будь-яке прохання переказати криптовалюту чи купити подарункові картки. Якщо ви вже надіслали гроші, негайно зв'яжіться з банком, а також повідомте місцеву поліцію і Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Judge: Accuracy: the source says "85 people ... reported losing"; "мешканців регіону" is fine. "Metro Vancouver" is rendered as "Метро-Ванкувер" (headline: "Метро-Ванкувері") and the headline keeps "RCMP" in Latin, while the glossary expects the full Ukrainian name on first mention, so the headline is a minor glossary slip. The lead and body are fine. "Сержантка" is fine. Minor: the source says "so far this year", rendered "Від початку року" (OK). "Кінна поліція" is correct. Language: "застерігає" and "зловмисники" are good. "Загалом вони втратили" is slightly choppy, and "Поліція називає ознаки обману" is fine. "Насторожити має" is slightly awkward (better "Має насторожити"). "Дипфейк" is explained in brackets, but "Підроблені обличчя й голос (дипфейк)" is a little clumsy. The headline mixes English and Ukrainian. Usefulness: clear and includes the actionable steps; it lacks a separate "what to do" section, but the advice is in the final paragraph. The headline uses "RCMP" instead of the Ukrainian name, and the Ukrainian audience may not know it.

### ucc-mentorship

**В Едмонтоні запустили програму наставництва для українців, які приїхали за CUAET**

Альбертська провінційна рада Конгресу українців Канади (КУК) запустила в Едмонтоні програму наставництва для українців, які приїхали до Канади за програмою CUAET.

Новоприбулим допомагатимуть 120 волонтерів. Здебільшого це канадські українці, які працюють у кваліфікованих робітничих професіях, медицині та інженерії. Наставник зустрічається зі своїм підопічним щонайменше двічі на місяць протягом шести місяців. Він допомагає шукати роботу, підтверджувати кваліфікацію, орендувати житло та заповнювати документи для державних установ. Програму фінансує приватний фонд Prairie Bridges Foundation із Калгарі: він виділив на неї 250 тисяч доларів на два роки.

Заявки від новоприбулих і від охочих стати наставниками приймають до 15 січня. Координаторка програми Галина Мороз (Halyna Moroz) каже: «Багато хто приїхав із добрим фахом, але не знає, як тут усе працює, а пояснити нікому. Наставник заощаджує місяці спроб і помилок».

Наступного року рада планує поширити програму на Калгарі, якщо вистачить коштів.

Judge: Facts match the source (120 mentors, twice a month for six months, $250,000 over two years, Calgary foundation, Jan 15, quote, Calgary expansion). Minor issues: the headline says "за CUAET" without the glossary form "програма CUAET" at first mention. "Альбертська провінційна рада" is slightly clumsy (better "Провінційна рада КУК в Альберті"). "кваліфікованих робітничих професіях" is a bit stiff for "trades". The Latin spelling of the coordinator's name in parentheses is unnecessary. "Заощаджує місяці" is slightly awkward. The post does not say how to apply, but the source gives no details either. Otherwise clear, concise and useful.

### ircc-cuaet-pr

**Українці, які приїхали за CUAET, зможуть подати заяву на постійне резидентство**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє нову програму постійного резидентства (PR) для українців, які приїхали до країни за програмою CUAET. Про це відомство повідомило в четвер.

Прийом заяв розпочнеться 2 березня. Міністерство прийме до 10 000 заяв. Заявник має відпрацювати в Канаді щонайменше рік на повну ставку після приїзду за CUAET і підтвердити знання мови: не нижче CLB 5 з англійської або NCLC 5 з французької. До заяви можна включити членів сім'ї, які перебувають у Канаді. Якщо заявник живе поза Квебеком, він також має намір оселитися за межами провінції: Квебек відбирає кандидатів самостійно.

Конгрес українців Канади (КУК) привітав рішення, але вважає ліміт надто малим. З 2022 року за CUAET приїхали понад 300 000 українців, і десятки тисяч із них досі мають тимчасовий статус.

Посібник із подання заяв і перелік потрібних документів міністерство імміграції оприлюднить за два тижні до відкриття програми.

Judge: Accuracy: the claim that tens of thousands still have temporary status is attributed in the source to the Congress ("the group says"). The post states it as fact. The 2 March start date and the 10,000 cap match the source. Language: "він також має намір оселитися" reads as a statement of fact. The source says "must also intend", so "повинен мати намір" is better. "Живе поза Квебеком" is slightly loose for "is outside Quebec". Usefulness: clear and covers the key conditions. It does not say that the time to prepare is short, and it does not mention that the guide comes before opening, which it does. No what-to-do advice, which is acceptable.

### statcan-population

**Населення Канади в третьому кварталі зросло найповільніше з 2020 року**

У третьому кварталі населення Канади зросло лише на 0,2 %. Це найповільніший приріст для цього періоду з 2020 року, повідомило Статистичне управління Канади (Statistics Canada).

Станом на 1 жовтня в країні налічувалося 41,7 млн людей. Зростання майже повністю забезпечили нові постійні резиденти. Кількість тимчасових резидентів, зокрема іноземних студентів і тимчасових працівників, скоротилася на 65 тисяч.

Це наслідок обмежень на видачу дозволів на навчання та змін у програмах тимчасової роботи, які Оттава оголосила протягом останніх двох років. Федеральний уряд заявив, що хоче зменшити частку тимчасових резидентів у населенні.

Серед провінцій найшвидше зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст не сягнув і 0,1 %.

Економісти зазначають, що повільніше зростання послабить тиск на ціни оренди у великих містах. Водночас у медицині та будівництві можуть загостритися проблеми з нестачею працівників.

Judge: Headline drops the qualifier "for that period" (third quarter), so it could be read as the slowest quarterly growth of any quarter since 2020. The body states it correctly. The post uses "тимчасові резиденти" for "non-permanent residents", which is acceptable. The body facts and numbers match the source, and the glossary name for Statistics Canada is used correctly. The Ukrainian is natural, with no calques. The post does not say what the change means for Ukrainians in Canada, such as newcomers, students, or people on temporary status, so it is clear but generic for this audience.

### akwesasne-policing

**Поліція могавків Аквесасне й OPP підписали угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) уклали п'ятирічну угоду про поліцейське обслуговування вартістю 12 млн доларів. Про це в понеділок повідомила рада.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) і OPP спільно патрулюватимуть річку та автошляхи поблизу громади. Вона розташована на перетині кордонів Онтаріо, Квебеку й штату Нью-Йорк. Гроші підуть також на будівництво нового поліцейського відділку на острові Корнвол (Cornwall Island) і підготовку восьми нових поліцейських.

Головна вождиня Лора Бенедикт (Laura Benedict) наголосила, що угода визнає поліцейських могавків першими, хто реагує на події в громаді. «Наші поліцейські знають ці води й ці родини. Це дає їм ресурси, щоб виконувати свою роботу», — сказала вона.

За словами OPP, влітку спільні патрулі зосередяться на боротьбі з контрабандою та безпеці плавання на човнах.

Judge: Accuracy: mostly faithful. Minor slip: "Вона розташована на перетині кордонів" – "Вона" is ambiguous, since the nearest antecedent is the river and highways, not the community. "Spільно патрулюватимуть" is fine. "Головна вождиня" for Grand Chief is acceptable but "Верховна/велика вождиня" is debatable. Source says "first responders", and "ті, хто реагує на події" is a bit loose. "Mohawk Council of Akwesasne" is correctly given as "Рада могавків Аквесасне". The Mohawk police are described as "поліцейські могавків", which is fine. "Гроші підуть... на будівництво" is OK: the source says "pay for a new station", so "будівництво" is a small addition. "Cornwall Island" is rendered as "острів Корнвол", which is nonstandard; "Корнуолл" is the usual Ukrainian form for Cornwall, ON. Language: mostly natural. "Зосередяться на боротьбі з контрабандою" is acceptable; "безпеці плавання на човнах" is a bit clumsy (better "безпеці на воді"). "Поліцейське обслуговування" is slightly calqued. "Угода визнає поліцейських могавків першими, хто реагує" is stiff. Usefulness: clear on what happened, but there is no explanation of why it matters to Ukrainians in Canada, and no context. That is acceptable for a straight news item but not strong.

### quebec-museum

**Музей сучасного мистецтва в Монреалі відкрився після ремонту**

У суботу для відвідувачів знову відкривається Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal). Реконструкція будівлі на Place des Arts тривала чотири роки й коштувала 40 млн доларів.

Виставкова площа збільшилася на 2000 квадратних метрів. З'явилися новий вхід з боку вулиці Сент-Катрин (Sainte-Catherine) і безкоштовна публічна тераса. Першої неділі кожного місяця вхід до музею буде вільним.

Першою виставкою стала оглядова виставка художниці Катерини Лисенко (Kateryna Lysenko). Вона народилася в Харкові, а з 1998 року живе в Монреалі. У залах представлено 60 робіт, зокрема серію великих полотен, створених після поїздки до рідного міста у 2023 році. «Я хотіла, щоб люди бачили Харків містом світла, студентів і музики, а не лише місцем із новин», — сказала Лисенко на попередньому перегляді в четвер.

Виставка триватиме до 12 квітня.

Judge: Accuracy: headline says the museum "відкрився" (already opened), but the source says it reopens on Saturday, so the tense is slightly off. The numbers, dates and names otherwise match. Language: "зокрема серію великих полотен" has the wrong case; it should be "зокрема серія". "Першою виставкою стала оглядова виставка" repeats the word "виставка". "Вхід... буде вільним" is slightly stiff. The title "Музей сучасного мистецтва Монреаля" is acceptable. Usefulness: it is clear and concise, and the Kharkiv link is relevant to this audience. It doesn't say explicitly why it matters to Ukrainians in Canada, and it has no practical details such as the address or hours, though the source doesn't give them.

### cra-ccb-tips

**Без декларації до 30 квітня допомогу на дітей припинять виплачувати**

Агенція доходів Канади (CRA) нагадує: щоб канадська допомога на дітей (CCB) надходила без перерв, обоє батьків мають подати податкову декларацію до 30 квітня. Це стосується й тих, хто торік не мав доходу.

Розмір допомоги щороку перераховують у липні на основі чистого доходу сім'ї за попередній рік. Якщо в CRA немає декларації когось із батьків, виплати припиняють у липні й поновлюють лише після того, як декларацію подадуть і опрацюють. Максимальна допомога на дитину до шести років зараз становить 8 157 доларів на рік.

Що можна зробити:
• Переконайтеся, що обоє з батьків подали декларацію, навіть якщо хтось із вас торік не мав доходу.
• Подайте декларацію заздалегідь, а не в останні дні квітня: її ще потрібно опрацювати.
• Якщо дохід невисокий, зверніться по безкоштовну допомогу до волонтерської податкової клініки у вашій громаді.
• Якщо ще не оформили CCB, подайте заявку в особистому акаунті CRA My Account.

Failed checks: facts: missing: RC66; glossary: not used: номер соціального страхування (SIN)

Judge: Accuracy: the source says "2026 income tax return", while the post omits the year (fine). "Both parents" is OK. Minor distortion: the source says $8,157 is the maximum "for a child under six", and the post's "на дитину до шести років" matches. The "Що можна зробити" list adds a claim, "file early because it must be processed", which is generally fine. The last bullet leaves out the SIN requirement and the mail option (RC66/RC66SCH), so the guidance for newcomers is incomplete. The post says "декларацію когось із батьків", which is fine. The post says payments stop "припиняють у липні", which matches the source. Headline "Без декларації ... припинять" is slightly absolute: the source says payments stop in July if the return is missing. Language: "в особистому акаунті" is a bit of an anglicism, and "особистий кабінет" would be more natural. "Агенція доходів Канади" follows the glossary. "доларів" without "канадських" is a minor point. "Обоє з батьків" is slightly clumsy. Usefulness: clear and concise, but SIN and newcomer details are missing. Source says "2026 return" with deadline April 30, which the post leaves out.

### health-canada-recall-tips

**Health Canada радить не використовувати дитячу суміш Maple Meadow через можливе забруднення бактерією Cronobacter**

Міністерство охорони здоров'я Канади (Health Canada) закликало батьків припинити використання трьох партій сухої дитячої суміші Maple Meadow. Вона може містити бактерію Cronobacter.

Це банки по 800 грамів із датою «найкраще вжити до» в червні 2027 року. Їх продавали в продуктових магазинах і аптеках по всій країні. Номери партій надруковані на дні банки. Про випадки захворювання поки не повідомляли.

Інфекція Cronobacter трапляється рідко, але може бути небезпечною для немовлят, особливо для недоношених і тих, хто має ослаблений імунітет. Її ознаки — гарячка, відмова від їжі, незвичний плач і сильна кволість.

Відкликаною сумішшю не можна годувати дитину. Банку варто повернути до магазину, де її купили, і отримати гроші назад. Якщо після такої суміші в дитини з'явилися симптоми, негайно зверніться до лікаря або зателефонуйте на 811.

Що можна зробити:
• Перегляньте дно кожної банки Maple Meadow, зокрема й нерозпочатих, і звірте номер партії з повідомленням Health Canada.
• Не викидайте банку з відкликаною сумішшю й збережіть чек, поки не повернете її до магазину.
• Якщо дитина вже їла таку суміш, запишіть, коли й скільки вона з'їла, та які з'явилися симптоми, — це знадобиться лікарю або 811.
• Розкажіть знайомим родинам із немовлятами про відкликання, особливо тим, хто міг купити цю суміш.

Failed checks: form: title too long; reviewer: Заголовок задовгий: у ньому 14 слів, а допустимо щонайбільше 12. Його треба скоротити.

Judge: Accuracy: the facts match the source. Two small issues. The headline says "Health Canada радить" (advises) and gives no Ukrainian name, so the glossary form is not used on first mention. The source's "very low energy" becomes "сильна кволість", which is acceptable. "Born early" is rendered as "недоношених", which is fine. The advice to keep the can and the receipt is sensible, but the source says to return the formula to the store, so keeping the can only until it is returned is consistent. The advice to record how much formula the baby ate and when is general and safe. Language: natural overall. "Гарячка" is acceptable, though "температура" or "жар" would be more usual. "Відмова від їжі" is a bit loose for "poor feeding" (слабке смоктання or поганий апетит would be closer). "Банку варто повернути до магазину" would be more natural as "у магазин". "Нерозпочатих" is a little awkward; "неВідкритих" would be better. The sentence "Про випадки захворювання поки не повідомляли" is fine. Usefulness: clear and practical, but the last bullet (tell friends) is mild padding. The first bullet says to check the lot number against the Health Canada notice, yet the post never says where to find the lot codes beyond the can bottom, and the source gives no lot numbers. This is a minor gap, not an invention.

