import random

def getRandomSentences():
    sentencesArr = [
        "Ki o tsukete",
        "Denwa no jama o shinaide kudasai",
        "Shukudai shite iru kara jama shinaide kure",
        "Watashi wa tsukarete iruyou desu",
        "Naniga attemo omaeo tasuketeyaru",
        "Anata no koto o itsu made mo wasurenai",
        "Watashi wa anata ga inai node, taihen sabishii",
        "Shinjireba, nanigoto mo kanou de aru",
        "Seikaku no yowa sa kanashimu nakare",
        "Sore wo nomu tokoro desu ka?",
        "Watashi wa nihongo ga sukoshi shika hanasemasen",
        "Nihongo wa hanasemasen",
        "Mou ichido onegaishimasu",
        "Aiteiru heya wa arimasu ka?",
        "Daiyokujou wa doko desu ka?",
        "Heya ni kagi wo wasuremashita",
        "O-susume no menu wa dore desu ka?"
        "Toire wa doko desu ka?",
        "Koko ni itte kudasai",
        "Anata wa nihonjin desu ka?",
        "Kurayami no tenshi",
        "Mijikai e-mail de gomen nasai",
        "Setchaku-zai ga arimasen",
        "Zettai yurusenai",
        "Sekai ni hitotsu dake no hana",
        "Anata no shashin o totemo ii desu ka?",
        "onaka ga suite imasu",
        "onaka ga ippai desu",
        "Yoroshiku onegai shimasu"
    ]

    pickedSentence = random.choice(sentencesArr)
    return pickedSentence