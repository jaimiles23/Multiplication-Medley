"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 09:41:25
 * @modify date 2020-05-13 15:49:40
 * @desc [
    Data file contains Speech Synthesis Markup Language (SSML) tags for Alexa skill.
 ]
 */
"""

##########
# Prosody
##########
MW_SLOW1 = """<prosody rate="97%">{}</prosody>"""
MW_SLOW2 = """<prosody rate="94%">{}</prosody>"""
MW_SLOW3 = """<prosody rate="91%">{}</prosody>"""
MW_SLOW4 = """<prosody rate="88%">{}</prosody>"""
MW_SLOW5 = """<prosody rate="85%">{}</prosody>"""

##########
# Excited
##########

EXCITED_LOW_START = """<amazon:emotion name="excited" intensity="low">"""
EXCITED_MED_START = """<amazon:emotion name="excited" intensity="medium">"""
EXCITED_HIGH_START = """<amazon:emotion name="excited" intensity="high">"""
EXCITED_END = """ </amazon:emotion>"""  

MW_EXCITED_LOW = """<amazon:emotion name="excited" intensity="low">{}</amazon:emotion>"""
MW_EXCITED_MED = """<amazon:emotion name="excited" intensity="medium">{}</amazon:emotion>"""
MW_EXCITED_HIGH = """<amazon:emotion name="excited" intensity="high">{}</amazon:emotion>"""


##########
# Domain
##########

MW_NEWS = """<amazon:domain name="news">{}</amazon:domain>"""
MW_MUSIC = """<amazon:domain name="music">{}</amazon:domain>"""
MW_DISAPPOINTED = """<amazon:emotion name="disappointed" intensity="medium">{}</amazon:emotion>"""


##########
# Emphasis
##########

MW_EMPHASIS =  """<emphasis level="moderate">{}</emphasis>"""


##########
# Speechcon
##########

MW_SPEECHCON = """<say-as interpret-as="interjection">{}!</say-as>"""

