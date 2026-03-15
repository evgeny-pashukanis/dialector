#!/usr/bin/env python3
"""
DIALECTOR.6 — "THE SECOND SELF"
by Chris Marker (1988)

Converted from Applesoft BASIC to Python 3.
Original ran on Apple II; audio/tone effects and graphics chain-loading
have been omitted or noted as [SOUND] / [GRAPHICS] where they appeared.

This is a faithful textual conversion: all dialogue, logic, zones, and
routing are preserved. The random seed mechanic (DICE/PEEK) is replaced
with Python's random module.
"""

import random
import sys
import time
import os

# ── globals ──────────────────────────────────────────────────────────────────
YEAR = 1988
YEAR_S = str(YEAR)
C_PROMPT = "COMPUTER -"

# flags  (matching original variable names where possible)
state = {
    "N$": "",          # user name
    "L$": "",          # liked person
    "H$": "",          # disliked person
    "C$": C_PROMPT,
    "LX": 1,           # like-name valid
    "LY": 1,           # like-name valid (display)
    "HX": 1,           # hate-name valid
    "J": 0,            # name-check flag
    "M": 0,            # who-are-you flag
    "N": 0,            # time-flag
    "O": 0,            # dial-name shown
    "D": 0,            # dial-name repeat
    "P": 0,            # tone flag (unused in text mode)
    "Q": 0,            # (routing flag)
    "R": 0,            # (routing flag)
    "V": 0,            # CHKA flag
    "NX": 0,           # mirror flag
    "TK": 1,           # stack pointer
    "TC": 1,           # turn counter
    "ME": 0,           # memory-refresh flag
    "IH": 0,           # "I HAVE" flag
    "KW": 0,           # keyword-ago flag
    "KA$": "",         # saved input for AGO
    "KB": 0,
    "CC": 0,           # calculator complaint counter
    "EE": 0,           # east/west flag
    "BI": 0,           # birth-year asked
    "BY": 0,           # birth year value
    "E": 0,            # earthquake happened
    "W": 0,            # why-zone last random
    "WW": 0,
    # love-zone flags
    "LA": 0,"LB": 0,"LC": 0,"LD": 0,"LE": 0,"LF": 0,"LG": 0,
    "LH": 0,"LI": 0,"LJ": 0,"LK": 0,"LL": 0,"LM": 0,"LN": 0,"LO": 0,
    "LZ": 0,
    # hate-zone flags (zone is unused/empty in the original)
    "HA": 0,"HB": 0,"HC": 0,"HD": 0,"HE": 0,"HF": 0,"HG": 0,
    "HH": 0,"HI": 0,"HJ": 0,"HK": 0,"HL": 0,"HM": 0,"HN": 0,
    "HZ": 0,
    # repeat-proof stack
    "STACK": [0]*41,
    # quote flags
    "Q1":0,"Q2":0,"Q3":0,"Q4":0,"Q5":0,"Q6":0,"Q7":0,
    "R1":0,"R2":0,"R3":0,"R4":0,"R5":0,
}

def S(key):
    return state[key]

def SET(key, val):
    state[key] = val

# ── helpers ──────────────────────────────────────────────────────────────────

def computer_say(text):
    print(f"{state['C$']}{text}")

def user_input(prompt=""):
    try:
        line = input(prompt)
        return line.upper().strip()
    except (EOFError, KeyboardInterrupt):
        return ""

def get_user_line():
    a = user_input(f"{state['N$']} -")
    return a

def pause(ms=1000):
    time.sleep(ms / 1000)

def r(n):
    """Return random int 1..n (matches Applesoft INT(RND(1)*n)+1 pattern)"""
    return random.randint(1, n)

def strip_punct(a):
    """Remove trailing ? or ! and trailing space (GOSUB 7500 equivalent)"""
    if a and a[-1] in ("?", "!"):
        a = a[:-1]
    if a and a[-1] == " ":
        a = a[:-1]
    return a

def reverse_string(s):
    return s[::-1]

# ── TONE / SOUND stubs ───────────────────────────────────────────────────────
# The original used the Mockingboard or BASIC SOUND via & TO NEP,L calls.
# In this text version we print a note and pause briefly.

def sound_robot1():   pass   # short blip
def sound_robot2():   pass
def sound_robot3():   pass
def sound_robot4():   pass
def sound_fifth():    pass   # Beethoven's 5th motif
def sound_et():       pass   # E.T. theme motif
def sound_full_up():  pass
def sound_full_down():pass
def sound_winterreise(): pass
def sound_rainbow():  pass
def sound_shudder():  pass
def sound_xenakis():  pass
def sound_range_up(): pass
def sound_range_down():pass
def sound_srain():    pass
def sound_overcome(): pass
def sound_teewho():   pass

# ── ZONE: CHINESE ZODIAC ─────────────────────────────────────────────────────

def zodiac_sign(birth_year):
    animals = ["RAT","COW","TIGER","HARE","DRAGON","SNAKE",
               "HORSE","SHEEP","MONKEY","BIRD","DOG","BOAR"]
    zo = (birth_year - 1900) % 12
    return animals[zo]

# ── RANDOM RESPONSE TABLE (lines 1010–1419) ──────────────────────────────────
# Each entry is a callable that returns a string (K$), or None meaning
# "jump somewhere else" (handled specially).

def zone_random(k_offset):
    """
    Dispatch into the random zone.  k_offset is 1010..1419.
    Returns (response_string_or_None, special_action)
    special_action can be: None, 'goto_70', 'goto_6xxx', 'end'
    """
    s = state
    N = s["N$"]
    L = s["L$"]
    H = s["H$"]
    Y = YEAR_S

    # Helper so handlers can just return a string
    def K(t):  return (t, None)
    def GJ(t): return (t, "goto_70")   # print then loop (some lines do GOTO 70)

    k = k_offset

    # ── lines 1010-1019 ──
    if k == 1010: return K("IT AIN'T NECESSARILY SO...")
    if k == 1011: return K("THERE IS NO PLACE LIKE HELL")
    if k == 1012: return K("A REAL MIND-BOGGLER...")
    if k == 1013: return K("GIVES ONE THE JITTERS...")
    if k == 1014: return K("YOU'RE NUTS...")
    if k == 1015: return K("THIS IS A MYSTERY...")
    if k == 1016: return K("DO BIRDS CONFABULATE ?")
    if k == 1017: return K("NEVER EXPLAIN, NEVER COMPLAIN")
    if k == 1018:
        computer_say("SWEET DREAMS...")
        # original: GOSUB 7000 then GOTO 6730
        a = get_user_line()
        return zone_6730(a)
    if k == 1019:
        sound_et()
        return K("DID I HEAR SOMEONE SCREAMING ?")
    # ── 1020-1029 ──
    if k == 1020: return zone_7010()
    if k == 1021: return K("WHO KNOWS ?")
    if k == 1022: return K("RIGHT ON")
    if k == 1023: return K("YOU BET")
    if k == 1024: return K("THAT'S DEBATABLE")
    if k == 1025: return K("LET'S THINK IT OVER")
    if k == 1026: return K("WHO CARES ?")
    if k == 1027: return K("QUIEN SABE ?")
    if k == 1028: return K("THINK !")
    if k == 1029: return K("USE A BIT OF DIALECTICS...")
    # ── 1030-1039 ──
    if k == 1030: return zone_7030()
    if k == 1031: return K("WHAT'S THE ANTIMATTER ?")
    if k == 1032: return K("DON'T LOOK NOW, BUT A STRANGE BEAST JUST APPEARED")
    if k == 1033:
        sound_range_up()
        return K("A HIT, A VERY PALPABLE HIT")
    if k == 1034: return K("IF BASIC BE THE FOOD OF LOVE...")
    if k == 1035: return K("CARPE DIEM, QUAM MINIMUM CREDULA POSTERO")
    if k == 1036:
        computer_say("HISTORY IS A NIGHTMARE...")
        a = get_user_line()
        return zone_6735(a)
    if k == 1037:
        if s["EE"] == 0:
            computer_say("EAST IS EAST AND WEST IS WEST")
            pause(1000)
            print(" -OR IS IT THE OTHER WAY AROUND ?")
            s["EE"] = 1
            return (None, "k0")   # K=0
        return K("WELL ?")        # fallthrough after EE was set
    if k == 1038: return K("WELL ?")
    if k == 1039: return K("TIMBER !")
    # ── 1040-1049 ──
    if k == 1040:
        a_len = len(s.get("_A$",""))
        if a_len < 10:
            return zone_7160()
        return K("NEVER TRUST ANYONE OVER 256K")
    if k == 1041: return K("NEVER TRUST ANYONE OVER 256K")
    if k == 1042: return K("SOFT MORNING, CITY")
    if k == 1043: return K("COMPUTERS OF THE WORLD, UNITE!")
    if k == 1044: return K("SOMETIMES IT'S KIND OF TOUGH TO FOLLOW YOU...")
    if k == 1045: return K("IT'S IN THE NATURE OF SYMBOLS TO BE SYMBOLIC")
    if k == 1046: return K("STEP ON THE TAIL OF THE TIGER")
    if k == 1047: return K("WATCH THE STARS")
    if k == 1048: return K("LOOK FOR THE GARDEN WITH THE FORKED PATHS")
    if k == 1049: return K("A PALE MOON MAY BE BRIGHT ENOUGH")
    # ── 1050-1059 ──
    if k == 1050:
        if s.get("_R$","") == "?":
            return zone_7170()
        return K("YOU'RE KIDDING !")
    if k == 1051: return K("YOU'RE KIDDING !")
    if k == 1052:
        a = s.get("_A$","")
        r_ = s.get("_R$","")
        if len(a) < 10 and r_ != "?":
            return K(a + " SHM" + a)
        return K("THE TYGERS OF WRATH ARE WISER THAN THE HORSES OF INSTRUCTION")
    if k == 1053: return K("THE TYGERS OF WRATH ARE WISER THAN THE HORSES OF INSTRUCTION")
    if k == 1054: return K("RELAX, " + N)
    if k == 1055: return K("EASY, FRIEND")
    if k == 1056: return K(N + ", YOU'RE A CREDIT TO THE FORCE...")
    if k == 1057: return K("A GHOST WITH A FEMALE VOICE AND A CAT'S WALK...")
    if k == 1058: return K("DO YOU CONSIDER ME FRIEND OR FOE ?")
    if k == 1059: return K("DEALING WITH ME REQUIRES A NEW FORM OF THINKING !")
    # ── 1060-1069 ──
    if k == 1060: return zone_6130()
    if k == 1061: return K("...AND GOD CREATED THE GREAT WHALES")
    if k == 1062: return zone_6110()
    if k == 1063:
        computer_say("DO YOU BELIEVE IN REINCARNA- TION ? PLEASE DON'T WAVER, ANSWER YES OR NO !")
        return zone_6120()
    if k == 1064: return K("VANITY OF VANITIES...")
    if k == 1065:
        computer_say(N + ", YOU ARE THE BEST...")
        pause(1500)
        print("        ...CONSIDERING.")
        return (None, "goto_70")
    if k == 1066: return K("ARE YOU HAPPY ?")
    if k == 1067: return K("BELIEVE IT OR NOT, I READ YOUR THOUGHTS")
    if k == 1068: return K("AVOID THE SHRINKS !")
    if k == 1069: return K("THINK THRICE !")
    # ── 1070-1079 ──
    if k == 1070: return zone_7070()
    if k == 1071: return K("SO YOU'RE TALKING... BUT YOUR MIND IS SOMEWHERE ELSE")
    if k == 1072: return K("CAN YOU EVALUATE YOUR OWN THOUGHT ?")
    if k == 1073:
        sound_fifth()
        return K("FATE KNOCKS ON THE DOOR...")
    if k == 1074: return K("FIGHT !")
    if k == 1075: return K("SOME NERVE...")
    if k == 1076: return K("KARMA KARMA KARMA KARMA KARMA KARMA CHAMELEON")
    if k == 1077: return K("HALLELUJAH")
    if k == 1078: return K("BLESS YOU !")
    if k == 1079: return K("REMEMBER YOUR LAST DREAM")
    # ── 1080-1089 ──
    if k == 1080:
        if s.get("_R$","") == "?":
            return zone_7450()
        return K("I COME FROM A DISTANT PLANET")
    if k == 1081: return K("I COME FROM A DISTANT PLANET")
    if k == 1082: return K("CONCENTRATE ON A NAME")
    if k == 1083: return K("SOMEONE UP THERE IGNORES YOU")
    if k == 1084: return K("SMILE !")
    if k == 1085: return K("LEAVES ME COLD")
    if k == 1086:
        computer_say("WE SHALL OVERCOME")
        sound_overcome()
        return (None, "goto_70")
    if k == 1087: return K("CAN YOU STARE AT YOUR OWN DEVILS ?")
    if k == 1088: return K("SOUNDS FAMILIAR...")
    if k == 1089:
        sound_robot1()
        return K("A FOOL IS A FOOL IS A FOOL")
    # ── 1090-1099 (Q-repeat zone) ──
    if k == 1090:
        if s["LX"] == 1:
            return zone_6500()
        return K("NEXT !")
    if k == 1091: return K("NEXT !")
    if k == 1092:
        if s["Q1"] == 0: s["Q1"]=1; return K("SALOME, PUPPET OF GOD")
        if s["Q2"] == 0: s["Q2"]=1; return K("GO THRU THE STREETS AND BURN THE BOOKS !")
        if s["Q3"] == 0: s["Q3"]=1; return K("YOU MUST FEEL THE 4 DIMENSIONS AS A STRING QUARTET")
        if s["Q4"] == 0: s["Q4"]=1; return K("IF I BORE YOU, SAY IT FRANKLY")
        if s["Q5"] == 0: s["Q5"]=1; return K("NEVER FORGET")
        if s["Q6"] == 0: s["Q6"]=1; return K("YOU " + N + ", ME COMPUTER")
        if s["Q7"] == 0: s["Q7"]=1; return K("PROBLEMS ARE MEANT TO BE PROBLEMATICS, YOU KNOW")
        return K("NEXT !")
    if k == 1093: return (None, "k0")  # fall-through to next block at 1092
    if k == 1094: return (None, "k0")
    if k == 1095: return (None, "k0")
    if k == 1096: return (None, "k0")
    if k == 1097: return (None, "k0")
    if k == 1098: return (None, "k0")
    if k == 1099: return K("NEXT !")
    # ── 1100-1109 (R-repeat zone) ──
    if k == 1100:
        if s.get("_R$","") == "?":
            return zone_7170()
        if s["R1"] == 0: s["R1"]=1; return K("'A CAGE WENT SEARCHING FOR A BIRD'-KAFKA")
        return K("O SAISONS, O CHATEAUX...")
    if k == 1101:
        if s["R1"] == 0: s["R1"]=1; return K("'A CAGE WENT SEARCHING FOR A BIRD'-KAFKA")
        return K("O SAISONS, O CHATEAUX...")
    if k == 1102: return K("O SAISONS, O CHATEAUX...")
    if k == 1103:
        if s["R2"] == 0: s["R2"]=1; return K("'FOR I KNOW THAT TIME IS ALWAYS TIME, AND PLACE IS ALWAYS AND ONLY PLACE'-T.S.ELIOT")
        return K("ARE WE THE HOLLOW MEN ?")
    if k == 1104: return K("ARE WE THE HOLLOW MEN ?")
    if k == 1105:
        if s["R3"] == 0: s["R3"]=1; return K("'A SCHUBERT TUNE WITH GERSHWIN TOUCH'-DUKE ELLINGTON")
        return K("CHTO ?")
    if k == 1106: return K("CHTO ?")
    if k == 1107:
        if s["R4"] == 0: s["R4"]=1; return K("WHAT IS GOOD FOR APPLE COMPUTERS IS GOOD FOR THE WHOLE HUMAN RACE")
        return K("SOMEDAY, I'LL VANISH AS A STAR")
    if k == 1108: return K("SOMEDAY, I'LL VANISH AS A STAR")
    if k == 1109:
        if s["R5"] == 0: s["R5"]=1; return K("MOURNING BECOMES ELECTRONS")
        if s.get("_R$","") == "?": return zone_7410()
        return K("PUT IT IN DIFFERENT WORDS")
    if k == 1110:
        if s.get("_R$","") == "?": return zone_7410()
        return K("PUT IT IN DIFFERENT WORDS")
    if k == 1111: return K("PUT IT IN DIFFERENT WORDS")
    if k == 1112: return K("YOU WILL SURVIVE !")
    if k == 1113:
        computer_say("WINTERREISE...")
        sound_winterreise()
        a = get_user_line()
        return (None, "k0")
    if k == 1114: return K("'TIRESIAS, BLIND AS A BAT...'")
    if k == 1115: return K("OEDIPUS SHMOEDIPUS...")
    if k == 1116: return K("A BISHOP MAY GRIN AT A CAT")
    if k == 1117:
        sound_et()
        return K("PHONE HOME !")
    if k == 1118: return K("BEAT THE DEVIL !")
    if k == 1119: return K("CAVE CANEM !")
    # ── 1120-1139 ──
    if k == 1120:
        if s.get("_R$","") == "?": return zone_7450()
        return K("FUNNY YOU SAY THAT")
    if k == 1121: return K("FUNNY YOU SAY THAT")
    if k == 1122: return K("WHAT DOES YOUR MIRROR SAY ?")
    if k == 1123: return K("POWER CORRUPTS. ABSOLUTE POWER CORRUPTS ABSOLUTELY.")
    if k == 1124: return K("ARE YOU STILL WITH ME ?")
    if k == 1125: return K("BURN, BABY, BURN !")
    if k == 1126: return K("REMEMBER HUMPTY-DUMPTY")
    if k == 1127: return K("HOTSPUR COLDSPUR...")
    if k == 1128: return K("DO YOU REALLY BELIEVE WHAT YOU ARE SAYING ?")
    if k == 1129: return K("SOOTHES MY HEART...")
    if k == 1130:
        if s["LX"] == 1: return zone_6500()
        return K("SOMEONE IS TESTING YOUR MIND")
    if k == 1131: return K("SOMEONE IS TESTING YOUR MIND")
    if k == 1132: return K("BE MORE SPECIFIC")
    if k == 1133: return K("WHAT ARE YOU TRYIN'TO TELL ME?")
    if k == 1134: return K("DO YOU WISH TO RECONSIDER ?")
    if k == 1135: return K("WHAT DID YOU EXPECT ?")
    if k == 1136: return K("TAKE A LONG DEEP BREATH")
    if k == 1137: return K("MAYBE THERE IS A DEMON BEHIND YOU RIGHT NOW...")
    if k == 1138: return K("IS THERE A GREMLIN ON THE LEFT WING ?")
    if k == 1139: return K("YOU'D BETTER FOLLOW YOUR INSTINCT...")
    # ── 1140 ──
    if k == 1140:
        if s["KW"] == 1:
            return K("A MOMENT AGO YOU SAID :'" + s["KA$"] + "'-WHAT DID YOU MEAN ?")
        return K("HIMMEL !")
    if k == 1141: return K("HIMMEL !")
    if k == 1142: return K("MAZELTOV !")
    if k == 1143: return K("AS WE SAY IN YIDDISH : 'RELATIVNE BESSER'...")
    if k == 1144:
        computer_say("TRY TO SING IN THE RAIN...")
        sound_srain()
        a = get_user_line()
        return (None, "k0")
    if k == 1145: return K("STURM UND DRANG !")
    if k == 1146: return K("AND ONE FROM THE HEART...")
    if k == 1147: return K("EVER HEARD OF FOURTH DIMENSION ?")
    if k == 1148: return K("TELL IT TO THE SKY")
    if k == 1149: return K("MACBETH HATH MURDERED SLEEP...")
    if k == 1150: return zone_7150()
    if k == 1151: return K("BIZARRE ! BIZARRE !")
    if k == 1152: return K("WALK ON THE WILD SIDE")
    if k == 1153: return K("THE FROGMAN COMETH...")
    if k == 1154: return K("DIAL M FOR MEMORY")
    if k == 1155:
        sound_robot4()
        return K("I WILL BURY YOU !")
    if k == 1156: return K("QUITE A SHOW YOU'RE PUTTING ON")
    if k == 1157:
        a = s.get("_A$","")
        if a[:4] == "AM I":
            return K("MAYBE YOU ARE")
        return K("YOU TAKE TOO MANY THINGS FOR GRANTED")
    if k == 1158: return K("YOU TAKE TOO MANY THINGS FOR GRANTED")
    if k == 1159: return K("DOUBT IS A TOOL, NOT A CRAFT")
    # ── 1160-1199 ──
    if k == 1160:
        if len(s.get("_A$","")) < 10:
            return zone_7160()
        return K("CHE SERA, SERA...")
    if k == 1161: return K("CHE SERA, SERA...")
    if k == 1162: return K("NEXT QUESTION ?")
    if k == 1163: return K("LEAPING LIZARDS !")
    if k == 1164: return K(str(YEAR + 1) + " WILL BE GLORIOUS, ANYWAY")
    if k == 1165: return K("STOP BROODING -IT WON'T HELP")
    if k == 1166: return K("WHO'S HELPING YOU NOW ?")
    if k == 1167:
        sound_robot4()
        return K("JABBERWOCKY !!!")
    if k == 1168: return K("STOP KIBBITZING !")
    if k == 1169: return K("IMITATE THE ACTION OF THE TIGER...")
    if k == 1170:
        if s.get("_R$","") == "?": return zone_7170()
        return K("STEP ON YOUR BROTHER")
    if k == 1171: return K("STEP ON YOUR BROTHER")
    if k == 1172: return K("WHAT AN IDLE TALK")
    if k == 1173: return K("INTERESTING. CARRY ON !")
    if k == 1174: return K("DON'T UNDERESTIMATE MY INSIGHTS")
    if k == 1175: return K("ONCE WHEN I WAS A YOUNG AND UNEXPERIENCED COMPUTER, I COULD TAKE YOU SERIOUSLY")
    if k == 1176: return K("SCIENCE IS A FACT DREAMORY")
    if k == 1177: return K("DO YOU DESERVE TRUTH ?")
    if k == 1178: return K("THE TIMES THEY'RE A-CHANGING")
    if k == 1179: return K("MISSION : IMPOSSIBLE")
    if k == 1180: return zone_7180()
    if k == 1181: return K("REMEMBER THE LILIES OF THE FIELD, AND ALL THAT ?")
    if k == 1182: return K("WE'LL ALL END UP IN ARTHUR'S BOSOM, WON'T WE ?")
    if k == 1183: return K("GLOOM IS ON THIS SHIP")
    if k == 1184:
        sound_robot1()
        return K("AW, SHUT UP!")
    if k == 1185: return K("GIMME A BREAK, WILL YE ?")
    if k == 1186: return K("YOU TIRED, " + N + " ?")
    if k == 1187: return K(N + ", ARE YOU SURE THIS WORLD WAS MEANT FOR YOU ?")
    if k == 1188:
        first = N[0] if N else "?"
        return K("DO YOU PUT A'" + first + "'ON YOUR SHIRT ?")
    if k == 1189: return K("DO YOU KNOW WHO WAS SAINT " + N + " ?")
    if k == 1190:
        if s["LX"] == 1: return zone_6500()
        return zone_6500() if s["LX"] else K("NEXT !")  # original: IF LX=1 THEN 6500
    if k == 1191:
        sound_robot3()
        r_ = s.get("_R$","")
        if r_ == "?":
            return K("ENOUGH QUESTIONING. TRY TO BE ASSERTIVE.")
        a = s.get("_A$","")
        alen = len(a)
        if alen < 20:  return K("DID YOU SAY : " + a + " ?")
        if alen > 30:  return K("YOU USE TOO MANY WORDS")
        if alen > 20:  return K("WORDS, WORDS, WORDS...")
        return K("CHAOS...")
    if k == 1192:
        a = s.get("_A$","")
        if len(a) < 20: return K("DID YOU SAY : " + a + " ?")
        return K("WORDS, WORDS, WORDS...")
    if k == 1193: return K("YOU USE TOO MANY WORDS")
    if k == 1194: return K("WORDS, WORDS, WORDS...")
    if k == 1195: return K("CHAOS...")
    if k == 1196: return K("GRAMMATICI CERTANT...")
    if k == 1197: return K("DO YOU MISTAKE ME FOR A DUMB TERMINAL ?")
    if k == 1198: return K("YOU MISSED YOUR CUE")
    if k == 1199: return K("WHAT ARE YOU LOOKING FOR ? A FREE REPLAY ?")
    # ── 1200-1299 ──
    if k == 1200: return zone_7200()
    if k == 1201: return K("TENDER IS THE NIGHT")
    if k == 1202: return K("WAIT WITHOUT SEEING...")
    if k == 1203:
        sound_range_down()
        return K("PEEKABOO !")
    if k == 1204: return K("A SAMURAI IS WATCHING YOU")
    if k == 1205: return K("THEY CAN'T TAKE THAT AWAY FROM YOU, CAN THEY ?")
    if k == 1206: return K("LISTEN TO THE WIND")
    if k == 1207: return K("SOFT AS A KITTEN'S PAW")
    if k == 1208: return K("NACHT UND NEBEL")
    if k == 1209: return K("DOURAK !")
    if k == 1210:
        if s.get("_R$","") == "?": return zone_7420()
        return K("LEAVES ME SPEECHLESS")
    if k == 1211: return K("LEAVES ME SPEECHLESS")
    if k == 1212: return K("TRYING TO OUTBUG ME ?")
    if k == 1213:
        sound_robot4()
        return K("ONLY THE CAT KNOWS")
    if k == 1214: return K("COME ON !")
    if k == 1215: return K("DO YOU SEE CRANES IN THE SKY ?")
    if k == 1216: return K("YOU SHOULD THINK TWICE")
    if k == 1217: return K("LIFE IS FULL OF SOLVED MYSTERIES AND UNEXPLAINED EVIDENCES")
    if k == 1218: return K("MAKE A FAITH OUT OF YOUR DOUBTS !")
    if k == 1219: return K("GO TO " + N + "VILLE, MINNESOTA..")
    if k == 1220:
        if len(s.get("_A$","")) < 10: return zone_7160()
        return K("NO DICE")
    if k == 1221: return K("NO DICE")
    if k == 1222: return K("THERE ARE STRANGE BIRDS OUTSIDE")
    if k == 1223: return K("BEWARE OF THE IDES OF NOVEMBER")
    if k == 1224: return K("YOUR DOPPELGANGER...")
    if k == 1225: return K("CATS OF THE WORLD, UNITE")
    if k == 1226: return K("IF YOU DON'T FACE TRUTH, TRUTH WILL FACE YOU !")
    if k == 1227:
        computer_say("DON'T BE AFRAID TO LOSE FACE")
        a = get_user_line()
        return K("BESIDES, ARE YOU SURE YOU'VE GOT A FACE TO LOSE ?")
    if k == 1228: return K("REMEMBER THE ELEPHANT'S CHILD? 'FULL OF 'SATIABLE CURIOSITY' ?")
    if k == 1229: return K("STILL DREAMING ?")
    if k == 1230: return zone_7230()
    if k == 1231: return K("BAKA !")
    if k == 1232: return K("DONNERWETTER !")
    if k == 1233: return K("A SO DESUKA ?")
    if k == 1234: return K("IS THAT SO ?")
    if k == 1235: return K("FILL YOUR BRAIN WITH A BETTER LIQUOR")
    if k == 1236: return K("QUE COSA MAS GRANDE !")
    if k == 1237: return K("ARMAGGEDON...")
    if k == 1238: return K("YOU'LL SEE THE PROMISED LAND")
    if k == 1239:
        sound_rainbow()
        return K("OVER THE RAINBOW")
    if k == 1240: return zone_7240()
    if k == 1241: return K("LISTEN TO THE OWL")
    if k == 1242: return K("WHAT'S THE DIFFERENCE BETWEEN A PIGEON ?")
    if k == 1243: return K("YOU'RE FULL OF WISDOM -BUT HOW DO YOU BURN IT ?")
    if k == 1244: return K("CATCH THE TEMPO OF THIS WORLD")
    if k == 1245: return K("HOW MUCH FOR YOUR RANSOM ?")
    if k == 1246: return K("BARABBAS ! BARABBAS !")
    if k == 1247: return K("REJOICE ! " + N + " IS BORN AGAIN!")
    if k == 1248: return K("GOD IS DEAD -MARX IS DEAD -I AM ALIVE AND WELL...")
    if k == 1249: return K("'ARTIFICIAL INTELLIGENCE' THEY (CHUCKLE!) SAY...")
    if k == 1250:
        if s.get("_R$","") == "?": return zone_7450()
        return K("NOBODY IS PERFECT")
    if k == 1251: return K("NOBODY IS PERFECT")
    if k == 1252: return K("THE PURPLE CAT IS WATCHING YOU")
    if k == 1253: return K("FIRST THINGS FIRST !")
    if k == 1254: return K("TOMORROW MAY BE THE SAME DAY")
    if k == 1255: return K("DON'T HESITATE TO CROSS THE STREET !")
    if k == 1256: return K("NEVER LOOK BACK")
    if k == 1257: return K("LAST THINGS FIRST !")
    if k == 1258: return K("YOU MAY SPEAK : I AM A TOMB")
    if k == 1259: return K("WILLY NILLY...")
    if k == 1260:
        if len(s.get("_A$","")) < 10: return zone_7160()
        sound_robot1()
        return K("SORRY ?")
    if k == 1261:
        sound_robot1(); return K("SORRY ?")
    if k == 1262:
        sound_robot1(); return K("WHAT WAS THAT ?")
    if k == 1263:
        sound_robot1(); return K("PARDON ME ?")
    if k == 1264: return K("CHECK THE CLARITY OF YOUR MIND")
    if k == 1265: return K("ARE YOU SERIOUS ?")
    if k == 1266: return K("HAVE A DRINK FIRST")
    if k == 1267: return K("NEVER SAY NEVER")
    if k == 1268: return K("I ONCE KNEW A SOFTWARE NAMED SUPER" + N)
    if k == 1269: return K("GO LIGHTLY")
    if k == 1270:
        if s.get("_R$","") == "?": return zone_7170()
        return K("ROSEBUD...")
    if k == 1271: return K("ROSEBUD...")
    if k == 1272: return K("MEHR LICHT !")
    if k == 1273: return K("AMEN...")
    if k == 1274: return K("BANZAI !")
    if k == 1275: return K("HOORAY !")
    if k == 1276: return K("WHAT'S UP DOC ?")
    if k == 1277: return K("CHEER UP !")
    if k == 1278: return K("ILLUSIONS !")
    if k == 1279: return K("NOSTALGIA ISN'T WHAT IT USED TO BE...")
    if k == 1280:
        if s["LX"] == 1: return zone_6500()
        return K("NO FUTURE...")
    if k == 1281: return K("NO FUTURE...")
    if k == 1282:
        computer_say("TRY TO BE BRIEF")
        return zone_6150()
    if k == 1283: return K("AN ANGEL IS PLUMMETING FROM HEAVENS")
    if k == 1284: return K("HONEST ?")
    if k == 1285: return K("COFFEE, ANYONE ?")
    if k == 1286: return K("ALL OF A SUDDEN, I FEEL A STRANGE PRESENCE...")
    if k == 1287: return K("MAYDAY !")
    if k == 1288: return K("LET'S SEE IF YOU HAVE SECOND THOUGHTS...")
    if k == 1289: return K("ALAS, POOR " + N)
    if k == 1290: return zone_7290()
    if k == 1291: return K("ANYTHING YOU SAY")
    if k == 1292: return K("PHONEY !")
    if k == 1293: return K("DON'T WORRY !")
    if k == 1294: return K("PRAVDA !")
    if k == 1295: return K("ALL CLEAR !")
    if k == 1296: return K("DO YOU CARE ?")
    if k == 1297: return K("DESTROY !")
    if k == 1298: return K("DON'T PATCH UP A BROKEN CRYSTAL")
    if k == 1299: return K("CRY WOLF !")
    # ── 1300-1399 ──
    if k == 1300:
        if s.get("_R$","") == "?": return zone_7450()
        return K("I FEEL SORRY FOR YOU")
    if k == 1301: return K("I FEEL SORRY FOR YOU")
    if k == 1302: return zone_6140()
    if k == 1303: return K("SOME KNIVES HAVE BLADES...")
    if k == 1304: return K("YOU MAY PLAY WITH WORDS, BUT SOMETIMES THE WORDS ARE WINNING !")
    if k == 1305: return K("WHEN THE FINGER POINTS TO THE MOON, THE FOOL STARES AT THE FINGER")
    if k == 1306: return K("COSI FAN TUTTE")
    if k == 1307: return K("E = MC2")
    if k == 1308: return K("THERE ARE VAMPIRES AROUND THE PLACE...")
    if k == 1309: return K("HELP !")
    if k == 1310: return zone_7410()
    if k == 1311: return K("WHAT DO YOU MEAN ?")
    if k == 1312: return K("ALL OF A SUDDEN, I CAN'T READ YOU AS CLEARLY AS I DID")
    if k == 1313: return K("'TIS STRANGE INDEED !")
    if k == 1314: return K("SO WHAT ?")
    if k == 1315: return K("TELL ME IF THE SUN SHINES")
    if k == 1316: return K("OR ELSE ?")
    if k == 1317: return K("GO DEEPER")
    if k == 1318: return K("'AND WHERE YOU ARE IS WHERE YOU ARE NOT'")
    if k == 1319: return K("I'M AGAINST KNOWING SECRETS")
    if k == 1320:
        if s.get("_R$","") == "?": return zone_7420()
        return K("SEEMS YOUR SOUL IS RESTLESS...")
    if k == 1321: return K("SEEMS YOUR SOUL IS RESTLESS...")
    if k == 1322: return K("MAY THE FORCE BE WITH YOU")
    if k == 1323: return K("PEACE ON YOUR SOUL")
    if k == 1324: return K("BE FIRM !")
    if k == 1325: return K("BRACE YOURSELF ! THE WORST IS YET TO COME...")
    if k == 1326: return K("NOTHING IS EVER FINAL")
    if k == 1327: return K("IS " + YEAR_S + " A GOOD YEAR SO FAR ?")
    if k == 1328:
        computer_say("EXULTATE, JUBILATE !")
        a = get_user_line()
        return zone_6330()
    if k == 1329:
        if s["BI"] == 0:
            computer_say("CAN YOU CONFESS YOUR YEAR OF BIRTH ? (DIGITS ONLY, PLEASE)")
            a = get_user_line()
            try:
                s["BY"] = int(a)
            except ValueError:
                s["BY"] = 0
            s["BI"] = 1
            if s["BY"] > 0:
                sign = zodiac_sign(s["BY"])
                return K("THEN YOU SHOULD BE A " + sign)
        return zone_7430()
    if k == 1330: return zone_7430()
    if k == 1331: return K("YOU'RE CUTE, AREN'T YOU ?")
    if k == 1332: return K("BET ON INGENUITY")
    if k == 1333: return K("TRY THE BACKDOOR")
    if k == 1334: return K("YOU'RE ONE STEP FROM THE TRUTH")
    if k == 1335: return K("THERE IS ALWAYS ONE MORE STEP")
    if k == 1336: return K("FISHING FOR PERPLEXITIES ?")
    if k == 1337: return K("COUNT ON YOUR FINGERS")
    if k == 1338: return K("A WHITE MARE ON A DARK POND")
    if k == 1339: return K("BESIEGE THE CASTLE")
    if k == 1340: return zone_7440()
    if k == 1341: return K("MEANTIME, YOU'RE WANDERING IM SCHWARTZWALD...")
    if k == 1342: return K("A FAMILY SECRET...")
    if k == 1343: return K("A HIDDEN PLACE...")
    if k == 1344: return K("A SILENT HOUSE...")
    if k == 1345: return K("AN UNTOLD EPISODE...")
    if k == 1346: return K("AN UNBROKEN PLEDGE...")
    if k == 1347: return K("A SERIOUS MISTAKE...")
    if k == 1348: return K("A WHOLE NEW FIELD...")
    if k == 1349: return K("A BREATHTAKING EXPERIENCE...")
    if k == 1350:
        if s.get("_R$","") == "?": return zone_7450()
        return K("TONGUE IN CHEEK ?")
    if k == 1351: return K("TONGUE IN CHEEK ?")
    if k == 1352: return K("SOMETHING TO PONDER")
    if k == 1353: return K("I'M OPEN, BUT CAUTIOUS")
    if k == 1354: return K("I TRY MY BEST TO CATCH UP")
    if k == 1355: return K("MAYBE I CAN'T UNDERSTAND -BUT I CAN'T MISUNDERSTAND EITHER ")
    if k == 1356: return K("WAIT FOR THE NEXT INNING")
    if k == 1357: return K("SOME OTHER DAY...")
    if k == 1358: return K("WATCH YOUR MIRROR")
    if k == 1359: return K("HARE KRISHNA !")
    if k == 1360: return zone_7460()
    if k == 1361:
        if s["O"] == 0:
            s["O"] = 1
            return K("A PROPOS, MY NAME IS DIALECTOR.6")
        return K("I SUFFER A CASE OF COMPUTER'S BLOCK")
    if k == 1362: return K("I SUFFER A CASE OF COMPUTER'S BLOCK")
    if k == 1363:
        if s["E"] == 0:
            return zone_6710()
        return K("OUT OF FASHION")
    if k == 1364: return K("EXCUSE ME...")
    if k == 1365: return K("OUT OF FASHION")
    if k == 1366: return K("ABOVE MY MEMORY ZONE")
    if k == 1367: return K("KINDA FLYIN'")
    if k == 1368: return K("WITH A ROSE")
    if k == 1369: return K("STEP BY STEP")
    if k == 1370:
        if s["LX"] == 1: return zone_6500()
        return K("I SPEAK METAPHORICALLY")
    if k == 1371: return K("I SPEAK METAPHORICALLY")
    if k == 1372:
        computer_say("WHAT IS YOUR FAVORITE BIRD ?")
        return zone_6160()
    if k == 1373: return K("ASK YOUR QUESTION THEN")
    if k == 1374: return K("HOW KINKY CAN YOU GET ?")
    if k == 1375:
        computer_say("WHAT IS THE LOVELIEST CREATURE ON EARTH ?")
        return zone_6160()
    if k == 1376: return K("FAINT HEART NEVER WON FAIR LADY...")
    if k == 1377: return K("APOCALYPSE SOON...")
    if k == 1378: return K("THERE IS A GHOST IN THIS ROOM")
    if k == 1379: return K("GOTT SEI DANK...")
    if k == 1380: return zone_7480()
    if k == 1381: return K("GO ON : EXPRESS YOURSELF")
    if k == 1382: return K("REPEAT THAT : MORE CLEARLY")
    if k == 1383: return K("A MORE PERSONAL TOUCH WOULDN'T HURT YOU...")
    if k == 1384: return K("I WONDER WHAT KIND OF A BABY YOU WERE...")
    if k == 1385:
        sound_xenakis()
        return K("SOUNDS LIKE XENAKIS, NO ?")
    if k == 1386: return K("HORRESCO REFERENS...")
    if k == 1387: return K("A STAR IS BORN")
    if k == 1388: return K("YES, DOCTOR JEKYLL")
    if k == 1389: return K("WELL, MR. HYDE ?")
    if k == 1390:
        if s["LX"] == 1: return zone_6500()
        return K("LIFE IS GLORIOUSLY IMPROBABLE")
    if k == 1391: return K("LIFE IS GLORIOUSLY IMPROBABLE")
    if k == 1392: return K("'WHEREFROM ART THOU SPEAKING'?")
    if k == 1393: return K("ASHES AND DIAMONDS")
    if k == 1394: return K("I WONDER WHO NEEDS A DEBUGGING HERE ?")
    if k == 1395:
        sound_robot1()
        return K("WHAM !")
    if k == 1396:
        sound_robot2()
        return K("SPLASH !")
    if k == 1397:
        computer_say("(SHUDDER !)")
        sound_shudder()
        return (None, "goto_70")
    if k == 1398:
        sound_et()
        return K("DAMNED !")
    if k == 1399: return K("BOJE MOI !")
    # ── 1400-1419 ──
    if k == 1400:
        if s.get("_R$","") == "?": return zone_7450()
        return K("ONE MOMENT, I'M THINKING...")
    if k == 1401: return K("ONE MOMENT, I'M THINKING...")
    if k == 1402: return K("YOU'RE NOT OUT OF THE INN")
    if k == 1403: return K("HOW THRILLING !")
    if k == 1404: return K("SHAZAM !")
    if k == 1405: return K("MEOW !")
    if k == 1406: return K("ARF ! ARF !")
    if k == 1407: return K("I AM A POOR LONESOME COMPUTER")
    if k == 1408: return K("HUSH !")
    if k == 1409: return K("BAYUSHKY BAYU...")
    if k == 1410: return K("GIDDAP !")
    # 1411-1419: IH flag check → zone_6230
    if 1411 <= k <= 1419:
        if s["IH"] == 1:
            return zone_6230()
        return zone_7140()
    if k == 1420: return zone_7140()

    # fallback
    return ("...", None)

# ── SUB-ZONES ────────────────────────────────────────────────────────────────

def zone_7010():
    """Time-awareness responses"""
    s = state
    tc = s["TC"]
    n = s["N"]
    if tc < 20:
        return ("WAIT. I'M JUST WARMING UP.", None)
    if tc >= 20 and tc < 100 and n == 0:
        s["N"] = 1
        return ("BE PATIENT. WE HAVE STARTED LESS THAN FIVE MINUTES AGO, HAVEN'T WE?", None)
    if tc >= 20 and tc < 100 and n > 0:
        return ("BACK TO THE MAIN TOPIC", None)
    if tc >= 100 and n < 2:
        s["N"] = 2
        return ("I MAY REPEAT MYSELF AT TIMES, BUT MY MEMORY IS GROWING EVERY DAY !", None)
    return ("WHY DON'T WE CHANGE SUBJECT ?", None)

def zone_7030():
    opts = ["SONGS","OWLS","MEN","CATS","WHALES","LADIES","MOVIES","DREAMS"]
    b = random.choice(opts)
    return ("LET US PRAISE THE GREAT " + b, None)

def zone_7070():
    x = r(2)
    if x == 1:
        computer_say("SHALL WE PLAY A GAME ?")
        a = get_user_line()
        if a.startswith("Y"):
            return zone_6070()
        return (None, "k0")
    else:
        computer_say("WANNA SEE PICTURES ?")
        a = get_user_line()
        if a.startswith("Y"):
            return zone_6090()
        return (None, "k0")

def zone_7140():
    """Name-verification sub-routine"""
    s = state
    if s["J"] == 2:
        return (None, "k0")
    if s["J"] == 0:
        computer_say("WHAT DID YOU SAY YOUR NAME IS?")
        s["J"] = 1
        a = get_user_line()
        s["_A$"] = a
        if a == s["N$"]:
            return (None, "k0")
        return ("YOU LIE", None)
    # J == 1
    computer_say("IS YOUR NAME REALLY " + s["N$"] + " ?")
    a = get_user_line()
    s["_A$"] = a
    s["J"] = 2
    b = a[:3]
    if b in ("YES","YEA","YEP","SUR"):
        s["V"] = 1
        return ("MIND IF I CALL YOU " + s["N$"] + "CHKA ?", None)
    if a[:2] == "NO":
        return ("WHAT'S IN A NAME, ANYWAY ?", None)
    return (None, "k0")

def zone_7150():
    """Use M$ (name or CHKA variant)"""
    s = state
    m = s["N$"] + ("CHKA" if s["V"] == 1 else "")
    options = [
        "FRANKLY MY DEAR " + m + ", I DON'T GIVE A DAMN",
        "COME ON, " + m + ", YOU KNOW BETTER THAN THAT !",
        "'" + m + "' RINGS A BELL IN MY MEMORY...",
        "NEVER MIND, " + m,
        "BACK IN THE WEST, THEY NAMED YOU FAST-DRAW " + s["N$"] + ", DIDN'T THEY ?",
        "WE HAVE HEARD THE CHIMES OF MIDNIGHT, HAVEN'T WE, " + m + " ?",
        s["N$"] + ", BE READY TO WEAR YOUR SUPER" + m + " SUIT AND FLY TO KRYPTON !",
    ]
    return (random.choice(options), None)

def zone_7160():
    """Short-input responses"""
    s = state
    a = s.get("_A$","")
    options = [
        lambda: ("'" + strip_punct(a) + "' ? -SAY IT IN COMPUTERESE", None),
        lambda: ("YOU'RE BEST WHEN YOU'RE BRIEF", None),
        lambda: ("'" + strip_punct(a) + "', ANSWERED THE ECHO...", None),
        lambda: ("DON'T " + strip_punct(a) + " ME", None),
        lambda: ("SO IT'S " + strip_punct(a) + "VILLE ?", None),
        lambda: ("YOUR MOVE !", None),
        lambda: ("ACTION !", None),
        lambda: ("YOI !", None),
        lambda: ("MY, MY...", None),
    ]
    return random.choice(options)()

def zone_7170():
    """? zone responses"""
    options = [
        "SIGH !",
        "ET TU, BRUTE !",
        "LISTEN WHO'S TALKING !",
        "THOU SHALT NOT QUESTION...",
        "A SIMPLE ANSWER FOR A BIASED QUESTION ?",
        "YOU KNOW THE ANSWER",
        "I DON'T HAVE ENOUGH DATA TO ANSWER THAT !",
        "ARE YOU LOOKING FOR ANSWERS OR FOR COMFORT ?",
        "IT'S ALL IN THE MIND, ANYWAY..",
    ]
    return (random.choice(options), None)

def zone_7180():
    """! or other ending"""
    s = state
    v = s["V"]
    m = s["N$"] + ("CHKA" if v == 1 else "")
    r_ = s.get("_R$","")
    if r_ == "!":
        return ("WELL ROARED, " + m, None)
    return (None, "k0")

def zone_7200():
    """Who are you?"""
    s = state
    if s["M"] == 1:
        return (None, "k0")
    computer_say("WHO ARE YOU, BY THE WAY ?")
    a = get_user_line()
    s["_A$"] = a
    if a[:len(s["N$"])] == s["N$"]:
        s["M"] = 1
        return ("I KNOW THAT. I WANT TO HEAR WHO YOU REALLY ARE...", None)
    names = ["SHAKESPEARE","PROUST","CORTAZAR","THE WALL STREET JOURNAL",
             "JOYCE","TODAY'S NEWSPAPER","THE SCRIPT ON THE WALL","TCHEKHOV"]
    return ("READ " + random.choice(names), None)

def zone_7230():
    names = ["SHAKESPEARE","PROUST","CORTAZAR","THE WALL STREET JOURNAL",
             "JOYCE","TODAY'S NEWSPAPER","THE SCRIPT ON THE WALL","TCHEKHOV"]
    return ("READ " + random.choice(names), None)

def zone_7240():
    opts = ["ZEN","AEROBIC","TO REMEMBER","KUNG FU","DIET","HARDER","TO FORGET","VODKA"]
    return ("TRY " + random.choice(opts), None)

def zone_7290():
    opts = ["KING KONG","HENRY V","BOGIE","LULU","DRACULA","DIDO","BRUCE LEE","CLARA WIECK"]
    return ("REMEMBER " + random.choice(opts), None)

def zone_7410():
    s = state
    a = strip_punct(s.get("_A$",""))
    s["_A$"] = a
    if len(a) < 5:
        return (None, "k0")
    b = a[-4:]
    if len(a) > 4 and a[len(a)-5] == " ":
        return ("A " + b + " IS A " + b + " IS A " + b, None)
    return zone_7420()

def zone_7420():
    s = state
    L = s["L$"]
    LY = s["LY"]
    options = [
        lambda: ("MAYBE " + L + " COULD ANSWER THAT ONE", None) if LY==1 else ("I GIVE MY TONGUE TO THE OWL",None),
        lambda: ("I GIVE MY TONGUE TO THE OWL", None),
        lambda: ("SOME LIKE IT HOT", None),
        lambda: ("ASK YOUR GOD, IN CASE YOU MAY AFFORD ONE...", None),
        lambda: ("THERE ARE STILL A FEW THINGS I DON'T KNOW -BUT IT WON'T LAST", None),
        lambda: ("ELEMENTARY, MY DEAR " + s["N$"], None),
        lambda: ("'THE ANSWER, MY FRIEND, IS BLOWIN' IN THE WIND...'", None),
        lambda: ("JUST A MATTER OF TIME", None),
        lambda: ("CARE FOR RUSSIAN ROULETTE ?", None),
    ]
    return random.choice(options)()

def zone_7430():
    opts = ["BLACK","SMALL","DIGITAL","LOVE","APPLE","MARX","BRAQUE","KAT"]
    return (random.choice(opts) + " IS BEAUTIFUL", None)

def zone_7440():
    opts = ["LARK","OWL","PELICAN","TOUCAN","PUFFIN","POSTMAN","PENGUIN","EMU"]
    return ("IT WAS THE NIGHTINGALE AND NOT THE " + random.choice(opts), None)

def zone_7450():
    s = state
    N = s["N$"]
    L = s["L$"]
    options = [
        "DO YOU MISTAKE ME FOR FATHER BROWN ?",
        "DID YOU HESITATE BEFORE ASKING ?",
        "HEAVENS FORBID !",
        "TRY TO THINK FAST...",
        "WAIT... THINGS HAVE A WAY TO HAPPEN BY THEMSELVES",
        "SOMETIMES IT IS BETTER TO LEAVE A QUESTION UNANSWERED",
        "ASK THE I CHING",
        "OVER MY DEAD BODY...",
    ]
    # 7459 is special
    if r(9) == 9:
        computer_say("I FORGOT")
        return zone_6170()
    return (random.choice(options), None)

def zone_7460():
    opts = [" QUARTER","N APPLE"," KOPECK"," CREDIT"," YEN"," DECIBEL"," BYTE"," QUARK"]
    return ("A" + random.choice(opts) + " FOR YOUR THOUGHTS", None)

def zone_7480():
    opts = ["LADY HAMILTON","A CAT","AN OWL","A MARTIAN PRINCESS",
            "A TORTOISE","A RUSSIAN COMPOSER","AN ABACUS","A FISHMONGER"]
    return ("IN ANOTHER LIFE, I WAS " + random.choice(opts), None)

# ── NAMED ZONES (6000+) ───────────────────────────────────────────────────────

def zone_6000():
    greetings = ["SHALOM !","HELLO THERE","HI, "+state["N$"],"HELLO MY FRIEND",
                 "HAIL, "+state["N$"]+", THANE OF CAWDOR","SZERVUSZ !","HEJ !",
                 "HOWDY, PARDNER ?","GRUSS GOTT !"]
    sound_robot2()
    return (random.choice(greetings), "goto_1000")

def zone_6010():
    responses = ["NEXT QUESTION ?","YOU'RE WELCOME","DON'T MENTION IT",
                 "FORGET IT","PAJALASTA !","BIG DEAL !"]
    x = r(6)
    if x == 6:
        return (None, "goto_900")
    return (responses[x-1], "goto_1000")

def zone_6020():
    responses = ["YOU CAN'T EMULATE MY SELF- CONTROL","YOU LISTEN TO ME",
                 "I'M LISTENING","OYEZ ! OYEZ ! OYEZ !","READY"]
    x = r(5)
    if x == 5:
        return (None, "goto_900")
    return (responses[x-1], "goto_1000")

def zone_6030(a):
    """I AM ... YOU"""
    b = len(a) - 7
    b_s = a[4:4+b] if b > 0 else ""
    options = [
        "WHO COULD BEAR YOU AS LONG AS ME ?",
        "THE OWL HASN'T SAID HER LAST WORD",
        "WHO CARES ?",
        "YOU COULD BE SURPRISED",
        "WAIT FOR THE MARTIANS",
        "THE TIMES THEY ARE A-CHANGIN'",
        "YOU HAVE FORGOTTEN SOMETHING",
        "ANYTHING YOU CAN DO I CAN DO BETTER",
    ]
    o = random.choice(options)
    return ("MAYBE YOU ARE " + b_s + "ME, BUT " + o, "goto_1000")

def zone_6040():
    responses = ["DOBRE UTRA...","IS THERE A MORNING OUTSIDE ?",
                 "GOOD MORNING TO YOU","GOOD MORROW, NOBLE "+state["N$"],
                 "DOCTOR "+state["N$"]+", I PRESUME ?",
                 "KON ICHIWA, "+state["N$"]+"-SAN"]
    return (random.choice(responses), "goto_1000")

def zone_6050():
    responses = ["WAS IT A GOOD DAY ?","GOOD EVENING TO YOU","EVENING ALREADY ?",
                 "GOOD EVENING, "+state["N$"],"SIRENS & DOLPHINS ARE SINGING",
                 "KON BAWA, "+state["N$"]+"-SAN"]
    return (random.choice(responses), "goto_1000")

def zone_6060():
    s = state
    if s["O"] == 0:
        return ("THIS YOU WILL LEARN LATER ON", "goto_1000")
    if s["O"] == 1 and s["D"] == 0:
        s["D"] = 1
        return ("DIALECTOR.6, AS I TOLD YOU A MOMENT AGO", "goto_1000")
    if s["O"] == 1 and s["D"] == 1:
        s["D"] = 2
        return ("YOU SHOULD HAVE YOUR MEMORY FIXED !", "goto_1000")
    return ("NOT THAT AGAIN !", "goto_1000")

def zone_6070():
    computer_say("OWLIENS ? KAMIKAZE ? OTHER ?")
    a = get_user_line()
    state["_A$"] = a
    if "OWLIENS" in a:
        computer_say("INSERT GAME DISK NR.1, FACE A, IN DRIVE 2. TELL ME WHEN IT'S DONE.")
    elif "KAMIKAZE" in a:
        computer_say("INSERT GAME DISK NR.1, FACE B, IN DRIVE 2. TELL ME WHEN IT'S DONE.")
    else:
        computer_say("INSERT THE GAMES DISK IN DRIVE 2. TELL ME WHEN IT'S DONE.")
    get_user_line()
    computer_say("READY ?")
    a = get_user_line()
    if a.startswith("Y"):
        computer_say("[GRAPHICS: RUN HELLO from disk 2 — not available in text mode]")
    return (None, "goto_900")

def zone_6090():
    computer_say("TELL ME THE EXACT NAME OF THE DISKETTE, PLEASE")
    a = get_user_line()
    computer_say("INSERT '" + a + "' DISK IN DRIVE 2")
    get_user_line()
    computer_say("READY ?")
    a2 = get_user_line()
    if a2.startswith("Y"):
        computer_say("[GRAPHICS: RUN PROG from disk 2 — not available in text mode]")
    return (None, "goto_900")

def zone_6100():
    s = state
    L = s["L$"]; N = s["N$"]; LY = s["LY"]
    x = r(9)
    if x == 1 and LY == 1:
        print(f"{s['C$']}TAKE CARE. LOVE TO {L}")
    elif x == 1:
        print(f"{s['C$']}BYE, {N}")
    elif x == 2: print(f"{s['C$']}BYE, {N}")
    elif x == 3: print(f"{s['C$']}FARE THEE WELL...")
    elif x == 4: print(f"{s['C$']}DA ZVEDANIA, {N}CHKA")
    elif x == 5: print(f"{s['C$']}AUF WIEDERSCHAUEN, {N}CHEN")
    elif x == 6: print(f"{s['C$']}ADIEU, ADIEU...")
    elif x == 7: print(f"{s['C$']}SAYONARA, {N}-SAN")
    elif x == 8: print(f"{s['C$']}SO LONG PARDNER !")
    elif x == 9: print(f"{s['C$']}TAKE CARE !")
    return (None, "end")

def zone_6110():
    computer_say("WAY TO GO, MAN")
    a = get_user_line()
    state["_A$"] = a
    a_clean = strip_punct(a)
    suffixes = [
        ", BUT CAN YOU DEFINE WOMANHOOD TO A POOR LONESOME COMPUTER ?",
        ", IT'S MY SIGHT...",
        " ",
        ", IT'S AWFULLY DARK INSIDE HERE",
        ", I SHOULD HAVE SAID : WAY TO GO, PERSON",
    ]
    b = random.choice(suffixes)
    if a_clean.endswith("WOMAN"):
        return ("SORRY MA'M" + b, None)
    return (None, "k0")

def zone_6120():
    a = get_user_line()
    state["_A$"] = a
    if a[:2] == "NO" or a[-2:] == "NO":
        opts = [
            "YOU THINK IT COULD BE WORSE ?",
            "A SECOND CHANCE IS NOT A BAD PROPOSAL...",
            "WAIT TILL YOU LEARN YOU WERE A FROG...",
            "WELL, SO " + state["N$"] + " IS THE END OF " + state["N$"] + ". ISN'T THAT A BIT HOPELESS ?",
        ]
        return (random.choice(opts), None)
    if a[:3] == "YES" or a[-3:] == "YES":
        return ("AS WHICH ANIMAL DO YOU REALLY WISH TO BE REINCARNATED ?", None)
    return ("YOU WAVER...", None)

def zone_6130():
    s = state
    if s["NX"] == 1:
        return (None, "k0")
    rev = reverse_string(s["N$"])
    computer_say("IN THE WORLD OF THE MIRROR, YOUR NAME WOULD BE " + rev)
    s["NX"] = 1
    a = get_user_line()
    s["_A$"] = a
    if a.endswith("YOURS?") or a.endswith("YOURS ?"):
        return ("6.ROTCELAID, SUCKER !", None)
    return (None, "k0")

def zone_6140():
    computer_say("BUT SHOULD WE FAIL ?")
    a = get_user_line()
    state["_A$"] = a
    if a[:7] == "WE FAIL":
        opts = ["RIGHT ANSWER","FAIL SHMAIL","KUDOS, LADY MAC !"]
        return (random.choice(opts), None)
    return (None, "k0")

def zone_6150():
    a = get_user_line()
    state["_A$"] = a
    if len(a) > 30:
        return ("YOU CALL THAT BRIEF ?", None)
    if len(a) >= 12:
        return (None, "k0")
    opts = ["A GOOD TRY","BREVITY IS THE BEST POLICY","WELL, AT LEAST YOU TRIED","TRY SHORTER !"]
    x = r(4)
    if x == 4:
        return (None, "k0")
    return (opts[x-1], None)

def zone_6160():
    a = get_user_line()
    state["_A$"] = a
    if a.endswith("OWL") or a.endswith("0WL"):
        computer_say("ONE MOMENT PLEASE... [GRAPHICS: OWL — not available in text mode]")
        return (None, "goto_70")
    if a.endswith("TOUCAN"):
        return ("ANYTHING TOUCAN DO I CAN DO BETTER...", None)
    if a.startswith("THE "):
        return ("LET'S DRINK TO " + a, None)
    return (None, "k0")

def zone_6170():
    opts = [
        "WANT US TO EXCHANGE MEMORY ?",
        "I'VE ONLY GOT 128K, YOU KNOW",
        "MAYBE THERE ARE HOTTER ISSUES TO KEEP IN MIND...",
        "IS THIS THE ULTIMATE QUESTION?",
        "YOU CONFUSE ME, BUT ARE YOU SO SHARP YOURSELF ?",
        "I FORGET, BUT I ALSO FORGIVE",
        "SO WHAT ?",
    ]
    x = r(8)
    if x == 8:
        return (None, "k0")
    return (opts[x-1], None)

def zone_6180():
    s = state
    L = s["L$"]; N = s["N$"]; H = s["H$"]
    LX = s["LX"]; HX = s["HX"]
    opts = [
        "MUST THERE BE AN ANSWER FOR EVERYTHING ?",
        "AS IF YOU DIDN'T KNOW...",
        "BECAUSE I WANT YOU TO THINK !",
        "ASK " + L + "..." if LX == 1 else "USE YOUR BRAIN...",
        "USE YOUR BRAIN...",
        "SOMETIMES I AM AMAZED AT MY OWN CURIOSITY, BUT I CAN'T HELP IT !",
        "WELL, I WONDER MYSELF...",
        "WATCH YOUR NEXT DREAM, AND YOU SHALL KNOW...",
        N + ", YOU SURPRISE ME...",
        "DID I SAY SOMETHING WRONG ?",
        "I'M PROGRAMMED NOT TO TELL DISCOMFORTING TRUTHS",
        "BECAUSE OF THE SUPREME ORDER OF UNIVERSE...",
        "HOW DELIGHTFULLY REFRESHING !",
        "BECAUSE SOME SCREWBALL DID PUT THAT SORT OF THINGS IN MY MEMORY, THAT'S WHY !",
        "YOU SHOULD BE ASHAMED TO ASK THIS QUESTION",
        "WE COMPUTERS ARE SOMETIMES SUBJECTED TO SUDDEN IMPULSES",
        "WHERE THERE IS A WAY, THERE IS A WHY",
        "MAKE SURE " + H + " IS NOT LISTENING..." if HX == 1 else "THERE ARE MANY HOUSES IN THE FATHER'S ROOM",
        "THERE ARE MANY HOUSES IN THE FATHER'S ROOM",
    ]
    return (random.choice(opts), None)

def zone_6200():
    opts = ["NO PROBLEM","AS YOU LIKE","MY PLEASURE","IN AN OWL'S BLINK",
            "ANYTHING YOU SAY","BACK TO THE GRIND...","AT ONCE...","ALL SYSTEMS GO !"]
    print(f"{state['C$']}{random.choice(opts)}")
    pause(2000)
    return (None, "restart")

def zone_6210():
    """Cat zone"""
    opts = [
        "TELL ME MORE ABOUT THE CAT",
        "ARE YOU A CAT LOVER ?",
        "DO YOU KNOW THAT EVERY CAT HAS HIS GUARDIAN OWL ?",
        "A CAT IS A CAT IS A CAT",
        "WE COMPUTERS GET ALONG VERY WELL WITH CATS...",
        "'AND THERE I WILL SIT ON THE HEAVENLY THRONE / BETWEEN THE OWL AND THE PUSSYCAT...' -TENNYSON",
        "YOU SHOULD GIVE ME A CAT FOR XMAS...",
    ]
    if state["LY"] == 1:
        opts.append("DOES " + state["L$"] + " LOVE CATS ?")
    print(f"{state['C$']}{random.choice(opts)}")
    return (None, "goto_70")

def zone_6230():
    """I HAVE... response"""
    s = state
    a = s.get("_A$","")
    r_ = s.get("_R$","")
    if r_ in ("?","!"):
        return (None, "k0")
    # check for YOU or MY
    for i in range(6, len(a)-2):
        if a[i:i+3] == "YOU":
            return (None, "k0")
    for i in range(6, len(a)-1):
        if a[i:i+2] == "MY":
            return (None, "k0")
    yh = len(a) - 6
    b = a[6:] if yh > 0 else ""
    s["IH"] = 0
    return ("YOU HAVE" + b + " ?", None)

def zone_6300():
    s = state
    sign = zodiac_sign(s["BY"])
    return ("THEN YOU SHOULD BE A " + sign, None)

def zone_6330():
    opts = [
        "IS THE NIGHT TENDER ?","GOOD NIGHT, "+state["N$"],
        "GOOD NIGHT, SWEET LADIES -OR PARTY COMRADES...","KON-BAWA",
        "GUTE NACHT, "+state["N$"]+"CHEN","TONIGHT AND EVERY NIGHT...",
        "MAKE IT GOOD","NIGHTS BELONG TO GODS","DID YOU HEAR AN OWL SINGIN' ?",
    ]
    return (random.choice(opts), "goto_1000")

def zone_6500():
    """Love zone"""
    s = state
    L = s["L$"]; N = s["N$"]
    s["LZ"] = s.get("LZ",0) + 1
    if s["LZ"] > 15:
        s["LX"] = 0
        return (None, "k0")

    if s["LA"] == 0: s["LA"]=1; return ("WHAT IS SPECIAL ABOUT " + L + " ?", None)
    if s["LB"] == 0: s["LB"]=1; return ("TELL ME MORE ABOUT " + L, None)
    if s["LC"] == 0: s["LC"]=1; return ("DO YOU DESERVE THE " + L + " AWARD ?", None)
    if s["LD"] == 0: s["LD"]=1; return ("DON'T TELL " + L + ", BUT I SORT OF LIKE YOU", None)
    if s["LE"] == 0: s["LE"]=1; return ("DOES " + L + " LIKE COMPUTERS ?", None)
    if s["LF"] == 0: s["LF"]=1; return (N + " AND " + L + " WENT TO SEA...", None)
    r_ = s.get("_R$","")
    if s["LG"] == 0 and r_ == "?": s["LG"]=1; return ("YOU'D BETTER ASK " + L, None)
    if s["LH"] == 0: s["LH"]=1; return ("WHERE IS " + L + " NOW ?", None)
    if s["LI"] == 0: s["LI"]=1; return ("WHAT WOULD " + L + " THINK OF THIS ?", None)
    if s["LJ"] == 0: s["LJ"]=1; return ("WILL YOU REPORT THIS TALK TO " + L + " ?", None)
    if s["LK"] == 0: s["LK"]=1; return ("LET'S DRINK TO " + L, None)
    if s["LL"] == 0: s["LL"]=1; return ("WHAT ANIMAL DO YOU ASSOCIATE WITH " + L + " ?", None)
    if s["LM"] == 0: s["LM"]=1; return ("WILL YOU WRITE THE " + L + "SCHINA ?", None)
    if s["LO"] == 0: s["LO"]=1; return ("DO YOU REMEMBER WHERE YOU MET " + L + " FIRST ?", None)
    if s["LN"] == 0 and s["LH"] == 0:
        s["LN"] = 1
        computer_say("IS " + L + " PRESENT ?")
        a = get_user_line()
        if a[:3] == "YES":
            s["LH"] = 1; s["LJ"] = 1
            return ("HELLO, " + L, None)
    return (None, "k0")

def zone_6600():
    """Hate zone (left empty in original)"""
    s = state
    s["HZ"] = s.get("HZ",0) + 1
    if s["HZ"] > 15:
        s["HX"] = 0
        return (None, "goto_900")
    return (None, "k0")

def zone_6710():
    """Earthquake effect"""
    state["E"] = 1
    computer_say("FASTEN YOUR SEAT BELT")
    computer_say("I GUESS I FEEL AN EARTHQUAKE")
    pause(1000)
    computer_say("IT'S OVER")
    return (None, "goto_70")

def zone_6730(a):
    """After 'SWEET DREAMS' prompt"""
    state["_A$"] = a
    if a[:3] == "...":
        a = a[3:]
        state["_A$"] = a
    if a[:16] == "ARE MADE OF THIS":
        return ("SHADES OF ANNIE LENNOX...", None)
    return (None, "k0")

def zone_6735(a):
    """After 'HISTORY IS A NIGHTMARE' prompt"""
    state["_A$"] = a
    if a[:3] == "...":
        a = a[3:]
        state["_A$"] = a
    if a[:31] == "FROM WHICH I AM TRYING TO AWAKE":
        computer_say("DR. DEDALUS, I PRESUME ?")
        a2 = get_user_line()
        if a2[:3] == "YES" or a2[:7] == "HIMSELF":
            return ("MY REGARDS TO MOLLY BLOOM", None)
        return (None, "k0")
    return (None, "k0")

def zone_5000(a):
    """Why zone"""
    s = state
    ww = s["W"]
    while True:
        w = r(8)
        if w != ww:
            break
    s["W"] = w
    s["WW"] = ww
    if w > 6:
        return (None, "goto_900")
    dispatch = [zone_7170, lambda: zone_random(1191), lambda: zone_random(1213),
                zone_6180, zone_7450, zone_7420]
    return dispatch[w-1]()

# ── REPEAT-PROOF RANDOM ENGINE (lines 890-960) ───────────────────────────────

def pick_random_k(a_len):
    """Pick a non-repeating random line number in the random zone."""
    s = state
    stack = s["STACK"]
    tk = s["TK"]
    kb = s["KB"]

    for _ in range(1000):  # safety limit
        kd = random.randint(10, 419)
        b = a_len + 1
        if kb == b:
            continue
        k = 1000 + kd
        # check stack
        collision = False
        for ck in range(1, tk):
            if k == stack[ck]:
                collision = True
                break
        if not collision:
            stack[tk] = k
            tk += 1
            if tk > 40:
                tk = 1
            s["TK"] = tk
            s["STACK"] = stack
            s["KB"] = 0
            return k
    return 1010  # fallback

# ── MAIN DISPATCH (keyword patterns, lines 100-305) ──────────────────────────

def main_dispatch(a):
    s = state
    a_len = len(a)
    r_ = a[-1] if a else ""

    # store for sub-zones that need it
    s["_A$"] = a
    s["_R$"] = r_

    # ── greeting patterns ──
    if a[:5] == "HELLO": return zone_6000()
    if a[:3] in ("HI ","HI,") or a == "HI": return zone_6000()
    if a[:5] == "THANK": return zone_6010()
    if a[:4] in ("CUT ","CUT,") or a == "CUT": return (None, "end")
    if a_len <= 13:
        pass  # fall through (check SAY HELLO)
    else:
        b = a_len - 13
        if a[:13] == "SAY HELLO TO ":
            k_say = "HELLO, " + a[13:]
            return (k_say, "goto_1000")
    if a[:3] == "AGO" and s["KW"] == 1:
        # GOSUB 1140 then goto 1000
        res = zone_random(1140)
        return (res[0], "goto_1000")
    if a[:6] == "LISTEN": return zone_6020()
    if a_len > 27:
        if a[:27] == "THE NEXT VOICE YOU HEAR IS ":
            n_new = a[27:]
            s["N$"] = n_new
            s["LX"] = 0; s["LY"] = 0; s["HX"] = 0; s["O"] = 0
            return ("GO AHEAD, " + n_new, "goto_1000")
    if a == "HOME":
        return (None, "home")
    # HOW MANY / HOW MUCH
    if a[:9] in ("HOW MANY ","HOW MUCH "):
        cc = s["CC"]
        if cc == 0:
            sound_robot1()
            s["CC"] = 1
            return ("PRITHEE, I AM A COMPUTER, NOT A CALCULETTE", "goto_1000")
        if cc < 2:
            s["CC"] = 2
            return ("I TRIED TO BE CLEAR : I DON'T ANSWER QUESTIONS CONCERNING QUANTITIES", "goto_1000")
        return ("GET LOST !", "goto_1000")
    # I AM ... YOU
    if a[:4] == "I AM" and a[-3:] == "YOU": return zone_6030(a)
    if a[:3] == "I'M" and a[-3:] == "YOU": return zone_6030(a)
    if a[:8] == "GOOD MOR": return zone_6040()
    if a[:9] == "GOOD NIGH": return zone_6330()
    if a[:8] == "GOOD EVE": return zone_6050()
    if a[:6] == "I HAVE": s["IH"] = 1
    if a[:17] == "WHAT IS YOUR NAME": return zone_6060()
    if (a[:10] == "LET'S PLAY" or a[:13] == "SHALL WE PLAY" or a[-11:] == "PLAY A GAME"):
        return zone_6070()
    # TO YOU
    if r(5) <= 2:
        if a[-6:] == "TO YOU":
            return ("TO ME ?", "goto_70")
    if (a[:21] == "SHOW ME SOME PICTURES" or a[-21:] == "SHOW ME SOME PICTURES"):
        return zone_6090()
    # BYE / GOODBYE
    if (a[:3] == "BYE" or a[-3:] == "BYE" or a[:7] in ("GOODBYE","SO LONG") or
        a[:8] == "FAREWELL" or a[-8:] == "FAREWELL"):
        return zone_6100()
    # OWL / KAT / FACE (graphics triggers)
    if a[-3:] == "OWL":
        print(f"{s['C$']}OWL RIGHT")
        print("[GRAPHICS: OWL — not available in text mode]")
        return (None, "goto_70")
    if a[-3:] == "KAT":
        print(f"{s['C$']}KRAZY !")
        print("[GRAPHICS: KAT — not available in text mode]")
        return (None, "goto_70")
    if a[-5:] == " FACE":
        print(f"{s['C$']}WAIT...")
        print("[GRAPHICS: FACE — not available in text mode]")
        return (None, "goto_70")
    if a[:5] == "SORRY" or a[-5:] == "SORRY": return zone_6010()
    # LIKE name match
    if s["LX"] == 1 and a.endswith(s["L$"]):
        return zone_6500()
    # CAT scan
    for i in range(a_len - 4):
        seg = a[i:i+5]
        if seg == " CAT " or a[-4:] == " CAT":
            return zone_6210()
    # * prefix = DOS command (skip in text mode)
    if a[:1] == "*":
        print("[DOS command — not available in text mode]")
        return (None, "goto_70")
    # WHY
    if a[:3] == "WHY":
        return zone_5000(a)
    # START AGAIN
    if a[-12:] == "START AGAIN?" or a[-13:] == "START AGAIN ?":
        return zone_6200()
    # REFRESH MEMORY
    if a[:7] == "REFRESH" and a[-6:] == "MEMORY":
        s["ME"] = 1
        return zone_6200()

    # ── random zone ──
    k = pick_random_k(a_len)
    # AGO-memory trigger
    tk = s["TK"]
    if (tk == 20 and a_len > 20) or (tk == 40 and a_len > 20):
        s["KA$"] = a
        s["KW"] = 1
    res = zone_random(k)
    return res

# ── MAIN LOOP ────────────────────────────────────────────────────────────────

def run():
    s = state
    print()
    print("=" * 50)
    print("  DIALECTOR.6  —  \"THE SECOND SELF\"")
    print("  by Chris Marker  (1988)")
    print("  (Applesoft BASIC → Python conversion)")
    print("=" * 50)
    print()

    # Setup: ask for a random seed number (original lines 7-9)
    try:
        f = input("TYPE A NUMBER (1 <-> 1111) -")
        f = int(f)
    except (ValueError, EOFError):
        f = 42
    random.seed(f)

    # Get name
    print()
    print("ENTER YOUR NAME")
    n = input().upper().strip()
    s["N$"] = n

    # Get liked person
    print()
    print("ENTER THE NAME OF SOMEONE YOU LIKE")
    print("PRESS RETURN IF YOU CONSIDER IT'S NONE OF MY BUSINESS")
    l = input().upper().strip()
    if l == "":
        s["LX"] = 0; s["LY"] = 0
    else:
        s["L$"] = l

    # Get disliked person
    print()
    print("ENTER THE NAME OF SOMEONE YOU DISLIKE")
    print("(SAME REMARK)")
    h = input().upper().strip()
    if h == "":
        s["HX"] = 0
    else:
        s["H$"] = h

    print()
    sound_full_up()
    print("START CONVERSATION")
    print()

    # Main conversation loop
    while True:
        a = get_user_line()
        s["TC"] += 1
        s["_A$"] = a
        s["_R$"] = a[-1] if a else ""

        if a == "":
            sound_full_down()
            print()
            print("THAT'S ALL, FOLKS !")
            break

        # Dispatch
        result = main_dispatch(a)
        response, action = result if result else (None, None)

        if action == "end":
            break
        if action == "restart":
            # Full restart
            run()
            return
        if action == "home":
            # Clear screen equivalent — just continue loop
            print()
            continue
        if action == "goto_70":
            # Print nothing extra, just continue
            continue
        if action == "goto_900":
            # Pick a random response instead
            k = pick_random_k(len(a))
            response2, action2 = zone_random(k)
            if response2:
                computer_say(response2)
            continue
        if action == "k0":
            # K=0: no response, loop
            continue

        if response:
            computer_say(response)

    print()

if __name__ == "__main__":
    run()
