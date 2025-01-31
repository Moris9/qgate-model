import datetime
import uuid
from generator.base_data import BaseData
from faker import Faker
from faker.providers import lorem
from generator.basic_party import BasicParty
from enum import Enum


class Sentiment(Enum):
    Positive = 1
    Negative = 2
    Neutral = 3
    Fake = 4

class BasicCommunication(BaseData):

    NAME = "07-basic-communication"
    COMMUNICATION_HISTORY_DAYS = 90

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicCommunication.NAME)
        self.fake = Faker(['en_US'])
        self.fake.add_provider(lorem)
        self.now = datetime.datetime.fromisoformat(self.gmodel["NOW"])

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # only 3 months back history
            # generate communication with history EVENT_HISTORY_DAYS
            party_customer=party['party-type'] == "Customer"
            communication_date = self.now - datetime.timedelta(days=float(BasicCommunication.COMMUNICATION_HISTORY_DAYS))

            # iteration cross days
            while True:

                # day for communication
                #   for customer:       more active (~ each 11 days)
                #   for non customer:   small amount of activities (~ each 19 days)
                if party_customer:
                    day = int(1.1 * self.rnd_choose(range(10),[0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.9]))
                else:
                    day = int(1.3 * self.rnd_choose(range(15), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.9]))
                communication_date = communication_date + datetime.timedelta(days=float(day))
                if communication_date > self.now:
                    break

                # define bundle
                #   for customer:       size 2-5x communications (bigger amount of activities)
                #   for non-customer:   size 1-3x communications (small amount of activites)
                session_id = str(uuid.uuid4())
                session_communications=self.rnd_choose(range(2, 5)) if party_customer else self.rnd_choose(range(1, 3))
                session_datetime = datetime.datetime(communication_date.year,
                                                     communication_date.month,
                                                     communication_date.day,
                                                     self.rnd_int(0,24),
                                                     self.rnd_int(0, 60),
                                                     self.rnd_int(0, 60))
                session_sentiment=self.rnd_choose([Sentiment.Neutral, Sentiment.Positive, Sentiment.Negative, Sentiment.Fake],
                                                       [0.6, 0.15, 0.05, 0.2])
                for event in range(session_communications):

                    # add new model
                    model = self.model_item()

                    # "name": "communication-id",
                    model['communication-id'] = str(uuid.uuid4())

                    # "name": "session-id",
                    model['session-id'] = session_id

                    # "name": "party-id",
                    model['party-id'] = party['party-id']

                    # "name": "content",
                    model['content'] = self._generate_text(session_sentiment)

                    # "name": "content-type",
                    model['content-type'] = "text"

                    # "name": "channel",
                    model['channel'] = self.rnd_choose(["email", "chat"], [0.8, 0.2])

                    # "name": "communication-date",
                    session_datetime = session_datetime + datetime.timedelta(seconds=float(self.rnd_int(0,13)))
                    model['communication-date']=session_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    # "name": "record-date"
                    model['record-date'] = self.gmodel["NOW"]

                    self.model.append(model)

    def _generate_text(self, sentiment: Sentiment) -> str:
        if sentiment==Sentiment.Positive:
            return self.positive_sentences[self.rnd_int(0, len(self.positive_sentences))]
        elif sentiment==Sentiment.Negative:
            return self.negative_sentences[self.rnd_int(0, len(self.negative_sentences))]
        elif sentiment==Sentiment.Neutral:
            return self.neutral_sentences[self.rnd_int(0,len(self.neutral_sentences))]
        else:
            return self.fake.sentence(nb_words = 15,variable_nb_words = True)

    # GenAI prompt
    # Write ten positive sentences or questions to the user support. The writer will be the satisfy or very satisfy user.
    # Write ten positive sentences or questions to the user support. The writer will be the satisfy or very satisfy user. The user support will be from travel agency.
    positive_sentences = [
        "I just wanted to say thank you for your amazing service. You really made my day!",
        "I'm very impressed with your product. It works flawlessly and has all the features I need. How can I leave a positive review?",
        "You are awesome! You solved my problem in no time and were very friendly and helpful. Can I speak to your supervisor and praise your work?",
        "I love your company. You always go above and beyond to meet my needs and expectations. Do you have a referral program that I can join?",
        "You have been very patient and informative with me. I appreciate your professionalism and expertise. Can you send me some additional resources to learn more about your product?",
        "I'm very happy with your service. You delivered on time, the quality was excellent, and the price was fair. Do you offer any discounts or coupons for loyal customers?",
        "You have exceeded my expectations. Your product is amazing and your support is outstanding. How can I share my feedback with other potential customers?",
        "You are the best! You answered all my questions and gave me some great tips and advice. Can I subscribe to your newsletter or blog to get more updates?",
        "I'm very grateful for your assistance. You were very courteous and respectful and handled my issue with care. Can I fill out a survey or a testimonial to express my satisfaction?",
        "You have made me a very happy customer. Your product is exactly what I was looking for and your support is top-notch. Do you have any other products or services that I might be interested in?",
        "I'm blown away by your product. It has transformed the way I work and saved me so much time and hassle. How can I spread the word about your amazing solution?",
        "You have been a lifesaver. You resolved my issue quickly and efficiently and followed up with me to make sure everything was working well. How can I rate your service and give you a glowing review?",
        "I'm thrilled with your service. You exceeded my expectations and delivered more than I asked for. How can I show my appreciation and gratitude to you and your team?",
        "You are a star. You listened to my needs and provided me with the best solution for my situation. How can I thank you and recommend you to others who might need your help?",
        "I'm very pleased with your product. It is easy to use, reliable, and has all the functionality I need. How can I stay updated on your latest features and developments?",
        "You have been a joy to work with. You were friendly, courteous, and professional throughout our interaction. How can I provide you with positive feedback and recognition for your excellent service?",
        "I'm ecstatic with your service. You went above and beyond to make me happy and satisfied. How can I reward you and show you my appreciation for your outstanding work?",
        "You are a gem. You answered all my queries and addressed all my concerns with patience and clarity. How can I express my satisfaction and admiration for your service and expertise?",
        "I'm very content with your product. It is high-quality, durable, and has a great design. How can I share my experience and opinion with other customers and potential buyers?",
        "You have been a delight to deal with. You were responsive, helpful, and knowledgeable throughout our communication. How can I compliment you and let your manager know how well you did?",
        "I am incredibly grateful for the unwavering support from our users",
        "Every milestone we achieve is a testament to the strong user support we receive.",
        "We are humbled by the overwhelming support from our users.",
        "I appreciate your prompt response to my queries.",
        "I am very pleased with the quality of service I have been receiving.",
        "The application has been running smoothly and efficiently.",
        "I appreciate the quick and helpful responses to my inquiries.",
        "The product delivers all the features as advertised, which is fantastic.",
        "The user interface is intuitive and easy to navigate.",
        "The clear instructions on your platform have been very helpful.",
        "I am impressed with the quality of your customer service.",
        "My issue was resolved promptly after my request, thank you for that.",
        "Your team’s exceptional service is a testament to the high standards of this organization.",
        "The unparalleled expertise of your support staff has left a lasting impression on me.",
        "I am in awe of your team’s ability to consistently deliver top-notch service.",
        "The extraordinary effort put forth by your team to resolve my issue was nothing short of commendable.",
        "Your team’s unwavering dedication to customer satisfaction is truly praiseworthy.",
        "The level of service provided by your team has set a new benchmark in customer support.",
        "I am profoundly grateful for the remarkable assistance provided by your team.",
        "The exemplary professionalism displayed by your support staff is a model for others to follow.",
        "Your team’s commitment to resolving customer issues is a shining example of excellent service.",
        "Thank you for providing an unparalleled customer service experience.",
        "Your team’s response time was impressive. How do you manage to be so efficient?",
        "The solution provided by your support team resolved my issue perfectly.",
        "I appreciate the professionalism and knowledge of your support staff.",
        "Your service exceeded my expectations. What other services do you offer?",
        "I am grateful for your team’s relentless effort in solving my problem.",
        "The user interface is very intuitive. Who designed it?",
        "Your product has significantly improved my productivity.",
        "I would like to commend your team for their excellent customer service.",
        "How can I leave a positive review for your outstanding service?",
        "Your product has made a significant difference in my work.",
        "The features of your software are very user-friendly.",
        "I am impressed by the seamless integration of your services.",
        "Your customer service is top-notch and highly commendable.",
        "The regular updates and improvements show your commitment to customer satisfaction.",
        "Your product is reliable and consistent, how do you maintain such high standards?",
        "I am amazed by the quick and efficient problem-solving by your team.",
        "The training resources provided by your team were very helpful.",
        "I am happy to recommend your services to others because of my excellent experience.",
        "Can I subscribe to your newsletter to stay updated with new features and services?",
        "Your assistance was incredibly helpful! Thank you!",
        "I’m so impressed with the quick response time. You’re doing an amazing job!",
        "Your team’s dedication to solving my issue is truly commendable.",
        "I appreciate your patience and understanding throughout this process.",
        "The level of professionalism here is outstanding.",
        "You’ve made my day brighter with your positive attitude!",
        "I’m genuinely satisfied with the service I received.",
        "Your attention to detail is remarkable.",
        "Keep up the fantastic work!",
        "How can I express how grateful I am? You’re awesome!",
        "Your energy is contagious—in the best way!",
        "You’re the reason ‘impossible’ becomes ‘I’m possible’.",
        "Thank you for making my travel experience so seamless and enjoyable.",
        "I was impressed with the quick response time when I had a question.",
        "The recommendations provided by your team were spot on and enhanced my trip.",
        "Could you please share more about the loyalty program? I’m interested in becoming a regular customer.",
        "The hotel you suggested was fantastic, do you have similar recommendations for my next trip?",
        "I appreciate the clear communication and updates throughout my journey.",
        "The itinerary was well-planned and allowed me to experience everything I wanted.",
        "How can I leave a review for the excellent service I received?",
        "I’m grateful for the assistance your team provided when my flight was delayed.",
        "Your team’s expertise and knowledge about the destination was truly beneficial.",
        "The travel package was worth every penny, thank you for such a great deal.",
        "Could you please let me know about any upcoming trips to Europe?",
        "I loved the personalized service and attention to detail.",
        "The travel guide provided was comprehensive and very useful.",
        "How can I recommend your agency to my friends and family?",
        "I appreciate the effort you put into ensuring my special dietary needs were met.",
        "The customer service was exceptional, especially the 24/7 support.",
        "I’m thankful for the smooth and hassle-free booking process.",
        "I’m excited about my future travels with your agency, keep up the good work!",
        "Thank you for the prompt and fair handling of my claim.",
        "I appreciate the clear and detailed explanation of the policy.",
        "The customer service provided was exceptional, making the process stress-free.",
        "Could you please inform me about any discounts on bundling policies?",
        "I’m grateful for the personalized advice that helped me choose the right coverage.",
        "The online portal is user-friendly and made managing my policy easy.",
        "I value the peace of mind that comes with having insurance from your company.",
        "I’m impressed with the professionalism and knowledge of your agents.",
        "Thank you for the reliable and timely service.",
        "I appreciate the professionalism and courtesy of your drivers.",
        "The cleanliness of the vehicles made my ride comfortable.",
        "Could you please let me know about any loyalty programs or discounts?",
        "I’m grateful for the easy booking process through your app.",
        "The GPS tracking feature gave me a sense of security during my journey.",
        "How can I rate my driver? They provided excellent service.",
        "I value the transparent pricing with no hidden charges.",
        "I’m impressed with the quick response time even during peak hours.",
        "I’m looking forward to using your service again, keep up the good work!",
    ]

    # GenAI prompt
    # Write ten negative sentences to the user support. The writer will be the user.
    # Write ten highly negative sentences to the user support. The writer will be the user.
    # Write ten trully negative sentences from bank environment to the user support. The writer will be the user.
    negative_sentences = [
        "Why is your product so slow and buggy? Fix it now or I'm leaving!",
        "You charged me twice for the same service! This is unacceptable! I want a refund immediately!",
        "Your agent was rude and unhelpful! I demand to speak to a manager!",
        "You promised me a delivery by yesterday, but I still haven't received my order! Where is it?",
        "Your website is down and I can't access my account! How long will this take to resolve?",
        "You sent me the wrong item! This is not what I ordered! How can you be so incompetent?",
        "Your product does not work as advertised! It's a scam! I want to cancel my subscription and get my money back!",
        "You keep sending me spam emails and calls! Stop harassing me or I'll report you!",
        "Your instructions are unclear and confusing! I can't figure out how to use your product! Help me or I'll switch to a competitor!",
        "You ignored my previous emails and chats! Don't you care about your customers? Respond to me now!",
        "I want to speak to your manager.",
        "I demand a refund.",
        "I want to cancel my subscription.",
        "I want to file a complaint.",
        "I want to know why this happened.",
        "I want to speak to someone who can help me.",
        "I want to know what you're going to do about this.",
        "I want to be compensated for my inconvenience.",
        "I want to know when this will be resolved.",
        "I want to speak to someone who can authorize a refund.",
        "I want to speak to someone who can fix this immediately.",
        "I want to know why I was charged for this.",
        "I want to speak to someone who can explain this to me.",
        "I want to know what you're going to do to make this right.",
        "I want to know why I wasn't informed about this issue.",
        "I want to speak to someone who can give me a clear answer.",
        "I want to know how you're going to prevent this from happening again.",
        "I want to know what you're going to do to compensate me for this.",
        "I want to speak to someone who can help me resolve this issue.",
        "I want to know what you're going to do to regain my trust.",
        "I want to know why I was charged twice.",
        "I want to know why my account was suspended.",
        "I want to know why my account was terminated.",
        "I want to know why my account was hacked.",
        "I want to know why my account was blocked.",
        "I want to know why my account was flagged.",
        "I want to know why my account was disabled.",
        "I want to know why my account was deleted.",
        "I want to know why my account was banned.",
        "I want to know why my account was locked.",
        "I'm experiencing an issue with my account.",
        "I am not satisfied with the level of service I have been receiving.",
        "The application has been crashing frequently, which is very frustrating.",
        "I have been overcharged for my subscription, which is unacceptable.",
        "The response time to my previous inquiries has been disappointingly slow.",
        "The product does not deliver the features as advertised.",
        "I am having a hard time navigating your user interface, it is not user-friendly.",
        "The lack of clear instructions on your platform is causing confusion.",
        "I am disappointed with the quality of your customer service.",
        "The frequent updates are disruptive and do not seem to improve the product.",
        "Despite my repeated requests, my issue has not been resolved.",
        "I’m disappointed with the recent changes in the product.",
        "The new update seems to have more bugs than improvements.",
        "I’ve been experiencing frequent crashes since the last update.",
        "The product doesn’t seem to meet the quality standards I expected.",
        "The customer service response time has been unsatisfactory.",
        "The user interface is not as intuitive as it used to be.",
        "The recent price increase doesn’t seem to be justified by the features offered.",
        "The product’s performance has been inconsistent recently.",
        "The lack of transparency in your policies is concerning.",
        "I feel that my feedback isn’t being taken into consideration.",
        "The product’s performance has been far below my expectations.",
        "The quality of the service provided has been disappointing.",
        "I’ve noticed a significant decline in the product’s reliability.",
        "The frequent technical issues have been frustrating.",
        "The product’s performance has been egregiously subpar, falling drastically short of the anticipated standards.",
        "The service provided has been lamentably deficient, failing to meet even the most basic expectations.",
        "The product’s reliability has been alarmingly inconsistent, leading to a significant loss of trust.",
        "The ostensible value proposition of the product does not align with its actual performance and quality.",
        "The customer service has been woefully inadequate, showing a lack of commitment to resolving customer issues.",
        "The product’s features are a far cry from the advertised standards, leading to a profound sense of disappointment.",
        "The persistent technical glitches have been a source of considerable frustration and inconvenience.",
        "The user interface of the product is remarkably unintuitive, necessitating a comprehensive overhaul.",
        "The exorbitant cost of the product is not justified by its mediocre quality and performance.",
        "The lack of efficient and responsive customer support is a glaring issue that needs immediate attention.",
        "The product’s performance is disappointingly inferior compared to its competitors.",
        "The quality of service is regrettably substandard when juxtaposed with industry standards.",
        "The product’s reliability is alarmingly inconsistent, especially when compared to previous versions.",
        "The customer service is lamentably unresponsive, particularly when contrasted with the prompt service provided by other companies.",
        "The features of the product are woefully inadequate, especially when compared to the advertised promises.",
        "The technical issues are significantly more frequent than what one would expect from a product of this caliber.",
        "The user interface is remarkably less intuitive than those of similar products in the market.",
        "The high cost of the product is unjustifiable, especially when compared to the superior quality offered by competitors at a similar price point.",
        "The lack of efficient customer support is glaringly evident when compared to the swift and effective support provided by other companies.",
        "The lack of professionalism displayed by the team is disheartening.",
        "The communication from the staff has been less than satisfactory.",
        "The team’s inability to meet deadlines consistently is concerning.",
        "The dismissive attitude towards customer feedback is not conducive to a healthy business relationship.",
        "The lack of transparency in the team’s operations raises questions about their integrity.",
        "The team’s reluctance to take responsibility for mistakes is disappointing.",
        "The unprofessional behavior displayed during meetings is unacceptable.",
        "The team’s lack of respect for differing opinions stifles innovation and growth.",
        "The lack of clear communication from the management leads to confusion and inefficiency.",
        "The team’s inability to handle criticism constructively hampers progress and improvement.",
        "I am curious about the measures you take to ensure the quality of your product.",
        "Could you please elaborate on the steps you take to rectify product mistakes?",
        "Your online banking system is a nightmare. It’s slow, clunky, and constantly crashes.",
        "I’ve been waiting on hold for over an hour. Your customer service is abysmal.",
        "Your fees are outrageous. I feel like I’m being robbed every time I use my account.",
        "I requested a simple account update, and it’s been weeks with no response.",
        "Your credit card declined, and I was left embarrassed at the checkout. Thanks a lot.",
        "Your mobile app is a disaster. It’s full of bugs and lacks basic features.",
        "I’ve been a loyal customer for years, and yet you treat me like I’m inconsequential.",
        "Your interest rates are laughable. Might as well stash my money under the mattress.",
        "Your loan approval process is a black hole. No transparency, no updates.",
        "Your bank charges for every little thing. It’s like death by a thousand cuts.",
    ]

    # GenAI prompt
    # Write ten neutral sentences or questions to the user support. The writer will be the user.
    # Write ten real neutral sentences or questions to the user support. The writer will be the user. The user support will be from travel agency.
    neutral_sentences = [
        "Thank you for your help.",
        "Could you please clarify this for me?",
        "I'm sorry, I didn't understand what you meant.",
        "I'm having trouble with this feature.",
        "Can you please guide me through the process?",
        "I'm not sure what to do next.",
        "I need help with a probably technical problem.",
        "I'm having difficulty accessing the website.",
        "Could you please help me with this feature?",
        "I'm sorry, I'm still having trouble with this.",
        "How do I create an account?",
        "What are the shipping options?",
        "How do I track my order?",
        "What is your return policy?",
        "How do I change my order?",
        "What payment methods do you accept?",
        "What is the warranty period?",
        "How do I change my password?",
        "What are the product specifications?",
        "How do I contact customer support?",
        "How can I check the status of my claim?",
        "What are the benefits and exclusions of my policy?",
        "How can I update my personal or payment information?",
        "How can I renew or cancel my policy?",
        "How can I get a quote or purchase a new product?",
        "What are the different types of insurance products you offer?",
        "How can I contact you if I have a question or complaint?",
        "How can I file a claim in case of an accident or emergency?",
        "What are the documents or proofs required for filing a claim?",
        "How can I get a copy of my policy document or certificate?",
        "How can I compare different insurance plans and prices?",
        "How can I get a discount or lower my premium?",
        "How can I access or download my insurance card or ID?",
        "How can I find a network provider or hospital near me?",
        "How can I get a refund or reimbursement for my expenses?",
        "How can I transfer or assign my policy to someone else?",
        "How can I get a confirmation or receipt for my payment?",
        "How can I get an extension or grace period for my payment?",
        "How can I open or close a bank account?",
        "How can I check my balance or transaction history?",
        "How can I transfer money or pay bills online?",
        "How can I apply for a loan or credit card?",
        "How can I change or reset my password or PIN?",
        "How can I report a lost or stolen card or cheque?",
        "How can I activate or deactivate my card or account?",
        "How can I order or deposit a cheque or cash?",
        "How can I update my contact or mailing address?",
        "How can I find an ATM or branch near me?",
        "How can I track or change the status of my shipment?",
        "How can I get a quote or estimate for my shipment?",
        "How can I schedule or cancel a pickup or delivery?",
        "How can I find or contact a service point or office?",
        "How can I create or print a shipping label or invoice?",
        "How can I claim or report a damaged or missing shipment?",
        "How can I request or verify a proof of delivery or signature?",
        "How can I manage or update my preferences or profile?",
        "How can I apply for a refund or compensation for my shipment?",
        "How can I get a customs clearance or declaration for my shipment?",
        "How can I redeem or earn rewards or points with my card?",
        "How can I increase or decrease my credit limit or spending power?",
        "How can I dispute or resolve a charge or fee on my card?",
        "How can I enroll or opt out of paperless statements or notifications?",
        "How can I add or remove an authorized user or joint account holder?",
        "How can I request or replace a new or damaged card?",
        "How can I access or manage my card account online or on the app?",
        "How can I set up or change a payment plan or due date for my card?",
        "How can I avoid or reduce interest or late fees on my card?",
        "How can I get a balance transfer or cash advance with my card?",
        "I am writing to inquire about the status of my account.",
        "Could you please provide me with more information about your services?",
        "I would like to know more about the features of your product.",
        "I am interested in upgrading my subscription, could you guide me through the process?",
        "I have noticed a discrepancy in my billing information and would like it to be rectified.",
        "Could you please clarify the terms and conditions of your service?",
        "I am unable to access certain features on your platform, could you please assist me?",
        "I am writing to inquire about the features of your product.",
        "Could you please provide more information about your services?",
        "I am interested in understanding the quality of your services.",
        "How can I get in touch with your user support team?",
        "Can you provide some insights into how your product compares to others in the market?",
        "I am looking forward to your response and appreciate your prompt attention to this matter.",
        "Can you help me understand how to use the main features of the product?",
        "What should I do if I forget my password?",
        "How can I change my account settings?",
        "What are the system requirements for this product?",
        "Can you guide me on how to upgrade to the latest version?",
        "What are the terms and conditions of the product’s usage?",
        "How does the product ensure the security and privacy of my data?",
        "What resources (like tutorials or guides) are available for learning more about the product?",
        "Hello, I’d like to inquire about my account balance.",
        "Could you please explain the fees associated with this savings account?",
        "Is there a way to set up automatic bill payments?",
        "What are the interest rates for a fixed-term deposit?",
        "I need assistance with updating my contact information.",
        "Can you guide me through the process of applying for a credit card?",
        "Is there a mobile app available for managing my accounts?",
        "Could you clarify the withdrawal limits for my checking account?",
        "I’m having trouble accessing my online banking. Can you help?",
        "What security measures are in place to protect my account?",
        "What destinations are currently popular for summer vacations?",
        "Could you provide information about available flights to Paris?",
        "Is there a cancellation policy for hotel bookings?",
        "What are the visa requirements for traveling to Japan?",
        "Can you recommend any guided tours for historical sites?",
        "Are there any travel insurance options for my upcoming trip?",
        "How do I check the availability of rental cars at my destination?",
        "What’s the best way to book a cruise vacation?",
        "Do you offer any discounts for group travel?",
        "Could you assist me with changing my flight dates?",
        "I would like to inquire about your rates for a trip from the airport to downtown.",
        "Can you please provide information on how to book a taxi in advance?",
        "I left my bag in one of your taxis, how can I retrieve it?",
        "Could you please explain your company’s policy on lost and found items?",
        "Can you provide information on the safety measures your company is taking during the COVID-19 pandemic?",
        "I am interested in setting up a corporate account, could you guide me through the process?",
        "What are the peak hours for your service and do you charge extra during these times?",
        "Do you have any special services or accommodations for passengers with disabilities?",
        "I would like to inquire about your flight schedules from New York to London.",
        "I left my bag on one of your flights, how can I retrieve it?",
        "I would like to inquire about your room rates for a two-night stay.",
        "Can you please provide information on how to book a room in advance?",
    ]
