# from fastapi import FastAPI, HTTPException
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel, Field
# from typing import Dict, List
# from openai import AsyncOpenAI # ใช้ AsyncOpenAI สำหรับ FastAPI
# import json
# import asyncio

# # ตั้งค่า OpenAI API Key
# client = AsyncOpenAI(api_key="??")
# app = FastAPI()

# class IssueDetail(BaseModel):
#     category: str
#     count: int = Field(..., gt=-1)
#     example_text: str

# class EventKPI(BaseModel):
#     event_name: str
#     location: str
#     event_detail: str
#     total_registered: int = Field(..., gt=0)
#     total_checked_in: int
#     total_feedback: int
#     occupations: Dict[str, int]
#     top_issues: List[IssueDetail]

# @app.post("/analyze-event-performance")
# async def analyze_event(kpi: EventKPI):
#     try:
#         if kpi.total_checked_in > kpi.total_registered:
#             raise ValueError("Checked-in count cannot exceed registered count")

#         # --- Calculation ---
#         check_in_rate = (kpi.total_checked_in / kpi.total_registered) * 100
#         feedback_rate = (kpi.total_feedback / kpi.total_checked_in) * 100 if kpi.total_checked_in > 0 else 0
#         top_occ = max(kpi.occupations, key=kpi.occupations.get)
#         issues_summary = "\n".join([f"- {i.category}: {i.count} รายการ ตัวอย่าง: {i.example_text}" for i in kpi.top_issues])

#         # prompt = f"""
#         # คุณคือผู้เชี่ยวชาญด้านการวิเคราะห์งานอีเว้นท์
#         # วิเคราะห์ผลการดำเนินงานของงาน: {kpi.event_name}
#         # สถานที่: {kpi.location}
#         # รายละเอียดงาน: {kpi.event_detail}
#         # สถิติ: Check-in {check_in_rate:.2f}%, Feedback {feedback_rate:.2f}%, กลุ่มหลัก {top_occ}
#         # ปัญหาที่พบ: {issues_summary}
#         # ช่วยสรุปภาพรวม 3 ประเด็น (Markdown ภาษาไทย)
#         # """

#         prompt = f"""
#         คำสั่ง: "ในฐานะที่ปรึกษาด้านการบริหารจัดการอีเวนต์ระดับมืออาชีพ ช่วยวิเคราะห์ข้อมูลสถิติจากระบบ EventHub และจัดทำ เอกสารสรุปผลการดำเนินงานหลังจบงาน (Post-Event Executive Report) บริบทของงาน: - ชื่องาน: [ระบุชื่องาน เช่น Tech Expo 2026]
#         ประเภทงาน: [งานจัดแสดงสินค้าและนวัตกรรม]
#         เป้าหมายหลัก: [เน้นการสร้าง Leads และความพึงพอใจของ Exhibitor]
#         [ข้อมูลสรุปจากระบบ (Data Input)]
#         {
#             "engagement_kpi": {
#                 "total_registered": 1200,
#                 "total_checked_in": 950,
#                 "check_in_rate": "79.17%",
#                 "role_distribution": {"Staff": 50, "Exhibitor": 150, "Visitor": 750},
#                 "gender_reach": {"Male": 450, "Female": 480, "Other": 20}
#             },
#             "satisfaction_kpi": {
#                 "overall_avg": 4.15,
#                 "visitor_score": 4.6,
#                 "exhibitor_score": 3.4,
#                 "top_scores_count": {"Rating_5": 520, "Rating_4": 280},
#                 "low_scores_count": {"Rating_1_2": 85}
#             },
#                 "operational_kpi": {
#                 "survey_completion_rate": "68%",
#                 "emails_sent": 1450,
#                 "returning_visitor_rate": "15%"
#             },
#             "feedback_summary_tags": [
#                 {"topic": "วิทยากร", "sentiment": "Positive", "mention_count": 320, "sample": "เนื้อหาดีมาก ทันสมัย"},
#                 {"topic": "สถานที่", "sentiment": "Negative", "mention_count": 180, "sample": "แอร์ในฮอลล์ไม่เย็นเลย คนเยอะจนอึดอัด"},
#                 {"topic": "ระบบลงทะเบียน", "sentiment": "Positive", "mention_count": 210, "sample": "สแกน QR Code เข้างานเร็วมาก สะดวก"}
#             ]
#         }

#         กรุณาสรุปรายงานตามโครงสร้างดังนี้:
#         สรุปภาพรวมความสำเร็จ (Executive Summary): วิเคราะห์ความสำเร็จเชิงปริมาณเทียบกับเป้าหมาย และการเข้าถึงกลุ่มเป้าหมาย (Demographic)
#         จุดแข็งที่โดดเด่น (Core Strengths): วิเคราะห์ปัจจัยที่ทำให้ได้รับคะแนนสูง และคำชมที่พบบ่อย (สิ่งที่ทำได้ดีแล้ว)
#         ปัญหาและอุปสรรคสำคัญ (Critical Issues): วิเคราะห์จุดที่ต้องปรับปรุงด่วน โดยเฉพาะความแตกต่างของคะแนน (Gap) ระหว่างกลุ่มผู้ใช้
#         แผนกลยุทธ์สำหรับงานถัดไป (Future Action Plan): เสนอแนวทางแก้ไขปัญหาและเทคนิคการเพิ่มยอด Engagement/Leads ในอนาคต
#         """

#         async def stream_generator():
#             # 1. ส่ง Metadata ออกไปก่อน
#             initial_data = {
#                 "status": "success",
#                 "metrics": {
#                     "check_in_rate": round(check_in_rate, 2),
#                     "feedback_rate": round(feedback_rate, 2)
#                 }
#             }
#             yield (json.dumps(initial_data) + "\n---\n").encode('utf-8')

#             # 2. เรียก GPT Stream
#             try:
#                 # เลือกโมเดล gpt-4o-mini หรือ gpt-4o
#                 response = await client.chat.completions.create(
#                     model="gpt-4o-mini", 
#                     messages=[
#                         {"role": "system", "content": "คุณคือที่ปรึกษาด้านการจัดการอีเว้นท์มืออาชีพ"},
#                         {"role": "user", "content": prompt}
#                     ],
#                     stream=True
#                 )

#                 async for chunk in response:
#                     content = chunk.choices[0].delta.content
#                     if content:
#                         yield content.encode('utf-8')
#                         await asyncio.sleep(0.01)

#             except Exception as e:
#                 yield f"\n[GPT Error: {str(e)}]".encode('utf-8')

#         return StreamingResponse(stream_generator(), media_type="text/event-stream")

#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         print(f"Server Error: {e}")
#         raise HTTPException(status_code=500, detail="Internal Processing Error")




# from fastapi import FastAPI, HTTPException
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel, Field
# from typing import Dict, List
# from openai import AsyncOpenAI
# import json
# import asyncio

# # ตั้งค่า OpenAI API Key (ควรเก็บไว้ใน environment variable เพื่อความปลอดภัย)
# client = AsyncOpenAI(api_key="???")
# app = FastAPI()

# class IssueDetail(BaseModel):
#     category: str
#     count: int = Field(..., gt=-1)
#     example_text: str
#     sentiment: str = "Negative"  # เพิ่มเพื่อให้ AI วิเคราะห์ Sentiment ได้ชัดเจนขึ้น

# class EventKPI(BaseModel):
#     event_name: str
#     event_type: str = "งานจัดแสดงสินค้าและนวัตกรรม"
#     location: str
#     event_detail: str
#     total_registered: int = Field(..., gt=0)
#     total_checked_in: int
#     total_feedback: int
#     role_distribution: Dict[str, int]  # เช่น {"Staff": 50, "Exhibitor": 150, "Visitor": 750}
#     gender_reach: Dict[str, int]      # เช่น {"Male": 450, "Female": 480, "Other": 20}
#     visitor_score: float = 0.0
#     exhibitor_score: float = 0.0
#     top_issues: List[IssueDetail]     # ข้อมูลจาก View V_AI_FEEDBACK_DATA
#     returning_visitor_rate: float = 0.0

# @app.post("/analyze-event-performance")
# async def analyze_event(kpi: EventKPI):
#     try:
#         if kpi.total_checked_in > kpi.total_registered:
#             raise ValueError("Checked-in count cannot exceed registered count")

#         # --- Data Preparation for Prompt ---
#         check_in_rate = (kpi.total_checked_in / kpi.total_registered) * 100
#         survey_completion_rate = (kpi.total_feedback / kpi.total_checked_in * 100) if kpi.total_checked_in > 0 else 0
#         overall_avg = (kpi.visitor_score + kpi.exhibitor_score) / 2

#         # สร้าง JSON Data Input สำหรับ Prompt
#         data_input = {
#             "engagement_kpi": {
#                 "total_registered": kpi.total_registered,
#                 "total_checked_in": kpi.total_checked_in,
#                 "check_in_rate": f"{round(check_in_rate, 2)}%",
#                 "role_distribution": kpi.role_distribution,
#                 "gender_reach": kpi.gender_reach
#             },
#             "satisfaction_kpi": {
#                 "overall_avg": round(overall_avg, 2),
#                 "visitor_score": kpi.visitor_score,
#                 "exhibitor_score": kpi.exhibitor_score,
#             },
#             "operational_kpi": {
#                 "survey_completion_rate": f"{round(survey_completion_rate, 2)}%",
#                 "returning_visitor_rate": f"{kpi.returning_visitor_rate}%"
#             },
#             "feedback_summary_tags": [
#                 {
#                     "topic": i.category,
#                     "sentiment": i.sentiment,
#                     "mention_count": i.count,
#                     "sample": i.example_text
#                 } for i in kpi.top_issues
#             ]
#         }

#         prompt = f"""
#         คำสั่ง: "ในฐานะที่ปรึกษาด้านการบริหารจัดการอีเวนต์ระดับมืออาชีพ ช่วยวิเคราะห์ข้อมูลสถิติจากระบบ EventHub และจัดทำ เอกสารสรุปผลการดำเนินงานหลังจบงาน (Post-Event Executive Report) 
        
#         บริบทของงาน:
#         - ชื่องาน: {kpi.event_name}
#         - ประเภทงาน: {kpi.event_type}
#         - สถานที่: {kpi.location}
#         - รายละเอียด: {kpi.event_detail}
#         - เป้าหมายหลัก: เน้นการสร้าง Leads และความพึงพอใจของ Exhibitor

#         [ข้อมูลสรุปจากระบบ (Data Input)]
#         {json.dumps(data_input, ensure_ascii=False, indent=2)}

#         กรุณาสรุปรายงานตามโครงสร้างดังนี้:
#         1. สรุปภาพรวมความสำเร็จ (Executive Summary): วิเคราะห์ความสำเร็จเชิงปริมาณเทียบกับเป้าหมาย และการเข้าถึงกลุ่มเป้าหมาย (Demographic)
#         2. จุดแข็งที่โดดเด่น (Core Strengths): วิเคราะห์ปัจจัยที่ทำให้ได้รับคะแนนสูง และคำชมที่พบบ่อย (สิ่งที่ทำได้ดีแล้ว)
#         3. ปัญหาและอุปสรรคสำคัญ (Critical Issues): วิเคราะห์จุดที่ต้องปรับปรุงด่วน โดยเฉพาะความแตกต่างของคะแนน (Gap) ระหว่างกลุ่มผู้ใช้
#         4. แผนกลยุทธ์สำหรับงานถัดไป (Future Action Plan): เสนอแนวทางแก้ไขปัญหาและเทคนิคการเพิ่มยอด Engagement/Leads ในอนาคต

#         สไตล์การเขียน: เน้นการวิเคราะห์เชิงลึก (Insightful), มีตัวเลขสนับสนุน (Data-Driven), และให้คำแนะนำที่นำไปปฏิบัติได้จริง (Actionable)
#         """

#         async def stream_generator():
#             # 1. ส่ง Metadata เริ่มต้น (Optional)
#             initial_meta = {
#                 "status": "processing",
#                 "event": kpi.event_name,
#                 "calculated_metrics": {
#                     "check_in_rate": round(check_in_rate, 2),
#                     "survey_rate": round(survey_completion_rate, 2)
#                 }
#             }
#             yield (json.dumps(initial_meta, ensure_ascii=False) + "\n---\n").encode('utf-8')

#             # 2. เรียก OpenAI Stream
#             try:
#                 response = await client.chat.completions.create(
#                     model="gpt-4o-mini", 
#                     messages=[
#                         {"role": "system", "content": "คุณคือที่ปรึกษาด้านการจัดการอีเว้นท์มืออาชีพที่วิเคราะห์ข้อมูลได้อย่างเฉียบคม"},
#                         {"role": "user", "content": prompt}
#                     ],
#                     stream=True
#                 )

#                 async for chunk in response:
#                     content = chunk.choices[0].delta.content
#                     if content:
#                         yield content.encode('utf-8')
#                         await asyncio.sleep(0.01)

#             except Exception as e:
#                 yield f"\n[AI Error: {str(e)}]".encode('utf-8')

#         return StreamingResponse(stream_generator(), media_type="text/plain")

#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         print(f"Server Error: {e}")
#         raise HTTPException(status_code=500, detail="Internal Processing Error")


# ... (ส่วน Imports และ Pydantic Models คงเดิม)

# @app.post("/analyze-event-performance")
# async def analyze_event(kpi: EventKPI):
#     try:
#         if kpi.total_checked_in > kpi.total_registered:
#             raise ValueError("Checked-in count cannot exceed registered count")

#         # --- Data Preparation ---
#         check_in_rate = (kpi.total_checked_in / kpi.total_registered) * 100
#         survey_rate = (kpi.total_feedback / kpi.total_checked_in * 100) if kpi.total_checked_in > 0 else 0
#         overall_avg = (kpi.visitor_score + kpi.exhibitor_score) / 2

#         data_input = {
#             "event_info": {
#                 "name": kpi.event_name,
#                 "type": kpi.event_type,
#                 "location": kpi.location
#             },
#             "engagement_stats": {
#                 "registered": kpi.total_registered,
#                 "checked_in": kpi.total_checked_in,
#                 "check_in_rate": f"{round(check_in_rate, 2)}%",
#                 "roles": kpi.role_distribution,
#                 "genders": kpi.gender_reach
#             },
#             "satisfaction_stats": {
#                 "overall_avg": round(overall_avg, 2),
#                 "visitor_score": kpi.visitor_score,
#                 "exhibitor_score": kpi.exhibitor_score,
#                 "returning_rate": f"{kpi.returning_visitor_rate}%"
#             },
#             "feedback_details": [
#                 {
#                     "topic": i.category,
#                     "sentiment": i.sentiment,
#                     "mentions": i.count,
#                     "sample": i.example_text
#                 } for i in kpi.top_issues
#             ]
#         }

#         # --- Enhanced Prompt for 10/10 Result ---
#         prompt = f"""
#         คำสั่ง: "ในฐานะที่ปรึกษาด้านการบริหารจัดการอีเวนต์ระดับมืออาชีพ และนักตรวจทานเอกสาร (Proofreader) ช่วยวิเคราะห์ข้อมูลจากระบบ EventHub และจัดทำ 'รายงานสรุปผลการดำเนินงานหลังจบงาน (Post-Event Executive Report)'

#         กฎเหล็กในการเขียน (Strict Execution Rules):
#         1. **ความถูกต้องของภาษา**: ใช้ภาษาไทยระดับทางการ ห้ามมีตัวอักษรภาษาอื่น (เช่น จีน, อังกฤษ) ปนมาในประโยคเด็ดขาด ตรวจสอบคำสะกดให้ถูกต้อง 100% (ห้ามสะกดผิด เช่น 'แตลง' หรือคำที่ไม่มีความหมาย)
#         2. **ห้ามใช้คำทับศัพท์**: ห้ามใช้คำว่า 'ซัมซิเปล', 'แชมเปิล', 'พอร์ต' หรือคำทับศัพท์ที่ระบุในข้อมูลดิบ ให้เปลี่ยนเป็นภาษาไทยที่เหมาะสม เช่น 'ตัวอย่างข้อความ', 'กรณีที่พบ', 'รายงาน' เป็นต้น
#         3. **ตรรกะข้อมูล**: ตรวจสอบให้แม่นยำระหว่าง 'จำนวนผู้ลงทะเบียน (Registered)' และ 'จำนวนผู้เช็คอิน (Checked-in)' ห้ามใช้สลับกัน และต้องระบุตัวเลขให้ตรงตามข้อมูลดิบเสมอ
#         4. **การวิเคราะห์เชิงลึก**: 
#            - ในส่วนประชากร (Demographics) ให้วิเคราะห์ว่าสัดส่วนที่พบส่งผลอย่างไรต่อทิศทางของงาน 
#            - ในส่วนของช่องว่าง (Gap) ต้องระบุชัดเจนว่าคะแนนกลุ่มใดที่ฉุดค่าเฉลี่ยลงมา

#         [ข้อมูลสรุปจากระบบ (Data Input)]
#         {json.dumps(data_input, ensure_ascii=False, indent=2)}

#         โครงสร้างรายงาน (ใช้ Markdown):
#         ## 1. บทสรุปผู้บริหาร (Executive Summary)
#         - วิเคราะห์จำนวนผู้ลงทะเบียนเทียบกับผู้เข้างานจริง และอัตราการเช็คอินที่ {round(check_in_rate, 2)}% เทียบกับมาตรฐานอุตสาหกรรม (70%)
#         - วิเคราะห์นัยสำคัญของสัดส่วนเพศและบทบาทของผู้เข้าร่วมงาน
        
#         ## 2. จุดแข็งและปัจจัยความสำเร็จ (Core Strengths)
#         - ระบุปัจจัยที่ทำให้ได้รับคะแนนสูง โดยเชื่อมโยงคะแนน Rating กับคำชมใน Feedback (เช่น คะแนนวิทยากรสูง สัมพันธ์กับคำชมเรื่องเนื้อหา)
        
#         ## 3. ประเด็นที่ต้องปรับปรุงเร่งด่วน (Critical Issues)
#         - วิเคราะห์ 'Stakeholder Gap' ระหว่างคะแนน Visitor และ Exhibitor อย่างละเอียด
#         - สรุปประเด็นเชิงลบที่วิกฤตที่สุด โดยระบุจำนวนครั้งที่ถูกกล่าวถึง (Mention Count) และตัวอย่างปัญหาอย่างชัดเจน
        
#         ## 4. ข้อเสนอแนะเชิงกลยุทธ์ (Future Action Plan)
#         - เสนอแนวทางแก้ไขปัญหาจากข้อ 3 แบบ 1-ต่อ-1 (เช่น ปัญหาแอร์ไม่เย็น แก้ด้วยการเพิ่มระบบทำความเย็นหรือเปลี่ยนสถานที่)
#         - กลยุทธ์การรักษาฐานผู้เข้าร่วมเดิม (Retention) และการดึงดูดกลุ่มใหม่ในงานถัดไป

#         สไตล์การเขียน: เฉียบคม, ภาษาทางการสละสลวย, มีข้อมูลสนับสนุนแม่นยำ, และนำไปปฏิบัติได้จริง"
#         """

#         async def stream_generator():
#             # ส่งผลการคำนวณเบื้องต้นออกไปก่อน
#             yield (json.dumps({"check_in_rate": round(check_in_rate, 2), "survey_rate": round(survey_rate, 2)}, ensure_ascii=False) + "\n---\n").encode('utf-8')

#             response = await client.chat.completions.create(
#                 model="gpt-4o-mini", 
#                 messages=[
#                     {"role": "system", "content": "คุณคือที่ปรึกษาด้านอีเวนต์ที่เชี่ยวชาญการวิเคราะห์ข้อมูลสถิติและสรุปกลยุทธ์"},
#                     {"role": "user", "content": prompt}
#                 ],
#                 stream=True
#             )

#             async for chunk in response:
#                 content = chunk.choices[0].delta.content
#                 if content:
#                     yield content.encode('utf-8')
#                     await asyncio.sleep(0.01)

#         return StreamingResponse(stream_generator(), media_type="text/plain")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, List
from openai import AsyncOpenAI
from openai import AsyncOpenAI
from dotenv import load_dotenv
import json
import asyncio
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# ตั้งค่า OpenAI API Client
client = AsyncOpenAI(api_key=api_key)

app = FastAPI()

class FeedbackDetail(BaseModel):
    category: str
    count: int = Field(..., gt=-1)
    example_text: str
    sentiment: str # "Positive" หรือ "Negative"

class EventKPI(BaseModel):
    event_name: str
    event_type: str = "งานจัดแสดงสินค้าและนวัตกรรม"
    location: str
    event_detail: str
    total_registered: int = Field(..., gt=0)
    total_checked_in: int
    total_feedback: int
    occupations: Dict[str, int]
    role_distribution: Dict[str, int] = {}
    gender_reach: Dict[str, int] = {}
    visitor_score: float = 0.0
    exhibitor_score: float = 0.0
    top_issues: List[FeedbackDetail] # ข้อมูลเชิงลบ
    top_good: List[FeedbackDetail]   # ข้อมูลเชิงบวก (ที่เพิ่มเข้ามา)
    returning_visitor_rate: float = 0.0

# --- Models ใหม่สำหรับการวิเคราะห์รายข้อ ---
class SuggestionInput(BaseModel):
    rs_id: str
    suggestion: str

class SuggestionAnalysisResponse(BaseModel):
    data: List[Dict[str, str]]

STANDARD_KEYWORDS = [
    # Venue & Facilities
    "สถานที่ (Venue)", "การเดินทาง (Accessibility)", "ที่จอดรถ (Parking)", 
    "ห้องน้ำ (Restroom)", "แอร์/อุณหภูมิ (Temperature)", "ความสะอาด (Cleanliness)", "ป้ายบอกทาง (Signage)",
    
    # Technology & Infrastructure
    "อินเทอร์เน็ต (WiFi)", "ระบบลงทะเบียน (Registration)", "แอปพลิเคชัน (Mobile App)", 
    "ระบบจองคิว (Queue System)", "ระบบเสียง/ภาพ (AV System)",
    
    # Staff & Service
    "เจ้าหน้าที่ (Staff)", "วิทยากร (Speaker)", "พิธีกร (MC)", 
    "การบริการ (Service)", "ความรวดเร็ว (Efficiency)",
    
    # Content & Activities
    "เนื้อหา (Content)", "เวิร์กชอป (Workshop)", "บูธแสดงสินค้า (Exhibitor)", 
    "ของสมนาคุณ (Giveaway)", "ระยะเวลา (Timing)",
    
    # Catering
    "อาหาร (Food)", "เครื่องดื่ม (Beverage)", "ความหลากหลาย (Variety)"
]

# --- Endpoint ใหม่: วิเคราะห์ Keyword & Sentiment ---
@app.post("/analyze-suggestions")
async def analyze_suggestions(inputs: List[SuggestionInput]):
    try:
        # เตรียมข้อมูล Input
        raw_data = [{"rs_id": item.rs_id, "text": item.suggestion} for item in inputs]
        
        # สร้าง String ของ Keyword มาตรฐานเพื่อส่งให้ AI
        keywords_str = ", ".join(STANDARD_KEYWORDS)

        prompt = f"""
        วิเคราะห์ข้อเสนอแนะจากงานอีเวนต์ โดยมีกฎเหล็กดังนี้:
        1. **Keyword**: ต้องเลือกใช้คำจากรายการ "STANDARD_KEYWORDS" ที่กำหนดให้เท่านั้น ห้ามคิดคำใหม่เองเด็ดขาด
        2. **Sentiment**: ระบุว่าเป็น Positive, Negative หรือ Neutral
        3. **Example Text**: ใช้ข้อความต้นฉบับที่ส่งมา

        รายการ STANDARD_KEYWORDS:
        [{keywords_str}, อื่นๆ (Other)]

        ข้อมูลที่ต้องวิเคราะห์:
        {json.dumps(raw_data, ensure_ascii=False)}

        ตอบกลับในรูปแบบ JSON:
        {{
          "data": [
            {{
              "rs_id": "string",
              "keyword": "ต้องตรงกับใน List เท่านั้น",
              "example_text": "string",
              "sentiment": "Positive/Negative/Neutral"
            }}
          ]
        }}
        """

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "คุณคือ AI ผู้เชี่ยวชาญด้านการจัดกลุ่มข้อมูล (Data Classification) ที่ทำงานได้อย่างแม่นยำและตอบเป็น JSON เท่านั้น"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0 # ตั้งเป็น 0 เพื่อให้ AI ทำตามกฎ Keyword อย่างเคร่งครัด
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/analyze-event-performance")
async def analyze_event(kpi: EventKPI):
    try:
        if kpi.total_checked_in > kpi.total_registered:
            raise ValueError("Checked-in count cannot exceed registered count")

        # --- การคำนวณพื้นฐาน ---
        check_in_rate = (kpi.total_checked_in / kpi.total_registered) * 100
        survey_rate = (kpi.total_feedback / kpi.total_checked_in * 100) if kpi.total_checked_in > 0 else 0
        overall_avg = (kpi.visitor_score + kpi.exhibitor_score) / 2
        top_occ = max(kpi.occupations, key=kpi.occupations.get) if kpi.occupations else "ไม่ระบุ"
        satisfaction_gap = abs(kpi.visitor_score - kpi.exhibitor_score)

        # --- เตรียม Data Input สำหรับ AI ---
        data_input = {
            "event_context": {
                "name": kpi.event_name,
                "type": kpi.event_type,
                "location": kpi.location,
                "detail": kpi.event_detail
            },
            "metrics": {
                "registered": kpi.total_registered,
                "checked_in": kpi.total_checked_in,
                "check_in_rate": f"{round(check_in_rate, 2)}%",
                "top_occupation": top_occ,
                "returning_rate": f"{kpi.returning_visitor_rate}%"
            },
            "satisfaction": {
                "visitor": kpi.visitor_score,
                "exhibitor": kpi.exhibitor_score,
                "average": round(overall_avg, 2)
            },
            "stakeholder_analysis": {
                "gap_score": round(satisfaction_gap, 2),
                "status": "Critical Imbalance" if satisfaction_gap > 0.5 else "Balanced"
            },
            "strengths": [
                {"topic": g.category, "mentions": g.count, "sample": g.example_text} 
                for g in kpi.top_good
            ],
            "weaknesses": [
                {"topic": i.category, "mentions": i.count, "sample": i.example_text} 
                for i in kpi.top_issues
            ]
        }
        prompt = f"""
        คำสั่ง: "ในฐานะที่ปรึกษาด้านการบริหารจัดการอีเวนต์ระดับมืออาชีพ และนักตรวจทานเอกสาร (Proofreader) ช่วยวิเคราะห์ข้อมูลสถิติจากระบบ EventHub และจัดทำ 'รายงานสรุปผลการดำเนินงานหลังจบงาน (Post-Event Executive Report)'

        กฎเหล็กที่ต้องปฏิบัติอย่างเคร่งครัด (Strict Execution Rules):
        1. **ความถูกต้องของภาษา**: ใช้ภาษาไทยระดับทางการ ห้ามมีตัวอักษรภาษาอื่น (เช่น จีน, อังกฤษ) ปนมาในประโยคเด็ดขาด และห้ามจบประโยคค้างไว้ ต้องสรุปให้จบกระบวนความ
        2. **ห้ามใช้คำทับศัพท์ที่ผิดเพี้ยน**: เปลี่ยนคำทับศัพท์เป็นภาษาไทยที่สละสลวย (เช่น ห้ามใช้ 'ซัมซิเปล', 'แชมเปิล', 'ถนอมนโยบาย' ให้ใช้ 'ตัวอย่างความเห็น', 'กรณีที่พบ', 'รักษามาตรฐานแนวทาง' ตามลำดับ)
        3. **ตรรกะข้อมูลและความแม่นยำ**: 
           - ตรวจสอบจำนวน 'ผู้ลงทะเบียน (Registered)' และ 'ผู้เช็กอิน (Checked-in)' ให้ถูกต้อง ห้ามใช้สลับกัน [ข้อมูลจริง: {kpi.total_registered} ลงทะเบียน, {kpi.total_checked_in} เช็กอิน]
           - วิเคราะห์ความย้อนแย้ง: หากหมวดหมู่ใดมีทั้งคนชมและคนบ่น (เช่น Registration) ให้วิเคราะห์ว่าเป็นปัญหาจากช่วงเวลา Peak Load หรือความไม่สม่ำเสมอของระบบ
        4. **วิเคราะห์ตามบริบท (Context-Aware)**: เชื่อมโยงปัญหาที่พบเข้ากับกลุ่มเป้าหมายหลัก (เช่น ปัญหา WiFi กระทบต่อกลุ่มนักศึกษาและนักพัฒนาที่ต้องใช้งานอินเทอร์เน็ตใน Workshop AI โดยตรง)
        5. การประยุกต์ใช้ทฤษฎีผู้มีส่วนได้ส่วนเสีย (Stakeholder Theory Implementation): ห้ามรายงานเพียงตัวเลขลอยๆ แต่ต้องวิเคราะห์ว่าความพึงพอใจที่ต่างกันระหว่าง Visitor และ Exhibitor ส่งผลต่อระบบนิเวศ (Ecosystem) ของงานอย่างไร โดยใช้หลักการสร้างสมดุล (Balance of Interests) เพื่อชี้ให้เห็นว่าความล้มเหลวในการตอบสนองความต้องการของกลุ่มหนึ่ง (เช่น Exhibitor) จะส่งผลกระทบลูกโซ่ต่อความยั่งยืนของงานในระยะยาว
        6. **ห้ามจบประโยคค้าง**: ตรวจสอบว่าประโยคสุดท้ายของรายงานสรุปจบอย่างสมบูรณ์และได้ใจความ
        7. **ตัวเลขคู่ขนาน**: ในบทสรุปผู้บริหาร ต้องระบุทั้งตัวเลขจำนวนคน (ลงทะเบียน/เช็กอิน) ควบคู่ไปกับค่าร้อยละ (%) เสมอ
        8. **วิเคราะห์ความขัดแย้งเชิงบวกและลบ**: หากหมวดหมู่ใดมีทั้งคนชมและคนบ่น ให้สรุปว่าเป็นปัญหาเฉพาะช่วงเวลา (เช่น ช่วงคนหนาแน่น) เพื่อความแม่นยำของข้อมูล
        9. **การสะกดคำ**: ตรวจสอบว่าไม่มีคำที่สะกดผิดหรือพยัญชนะหล่นหายแม้แต่ตัวเดียว
        10. **เจาะลึก Stakeholder Gap**: ต้องวิเคราะห์เปรียบเทียบความพึงพอใจระหว่าง Visitor และ Exhibitor อย่างชัดเจนจากคะแนนที่มีและสรุปว่าความแตกต่างนี้ส่งผลต่อความยั่งยืนของงานอย่างไร
        12. **สรุปความสัมพันธ์ 1-ต่อ-1**: ในแผนกลยุทธ์ (Future Action Plan) ต้องระบุวิธีแก้ปัญหาที่ล้อตาม Critical Issues ในข้อ 3 แบบเป็นข้อๆ ให้ครบถ้วน
        13. **วิเคราะห์ความคาดหวังกลุ่มเป้าหมาย**: เชื่อมโยงว่าทำไม WiFi ถึงสำคัญต่อนักศึกษาใน Workshop AI เพื่อเพิ่มน้ำหนักให้กับการวิเคราะห์ปัญหา

        กฎเหล็กที่ต้องย้ำ (The Final Guardrails):
        1. **ห้ามลืมตัวเลขดิบ**: ในข้อ 1 (Executive Summary) ต้องเขียนว่า "มีผู้ลงทะเบียนจำนวน {kpi.total_registered} คน และเข้างานจริง {kpi.total_checked_in} คน คิดเป็น {round(check_in_rate, 2)}%" เสมอ
        2. **ความถูกต้องของคำศัพท์**: ตรวจสอบการใช้คำว่า "เช็กอิน" (ใช้ ก ไก่) และ "เสถียรภาพ" ให้ถูกต้องตามหลักภาษาไทยทางการ
        3. **ความต่อเนื่องของตาราง**: ในตาราง Dashboard ช่อง 'สถานะ' สำหรับคะแนนความพึงพอใจ: 4.0 ขึ้นไปให้ ✅, 3.5-3.9 ให้ ⚠️, ต่ำกว่า 3.5 ให้ 🚨 และหากเกิด Strategic Imbalance (Gap > 0.5) ให้ติด ⚠️ ในช่อง Interpretation กำกับด้วย
        4. **ห้ามมีคำภาษาอังกฤษหลุดรอด**: หากต้องใช้คำทับศัพท์ เช่น WiFi หรือ AI ให้เขียนด้วยตัวพิมพ์ใหญ่ตามมาตรฐานสากล แต่เนื้อหาแวดล้อมต้องเป็นไทย 100%
        5. การปิดจบรายงาน: ต้องสรุปปิดท้ายด้วยประโยคที่แสดงถึงความมุ่งมั่นในการพัฒนาโครงการให้ดียิ่งขึ้นในอนาคต และตรวจสอบให้แน่ใจว่าไม่มีอักขระตัวสุดท้ายตัวใดขาดหายไป
       
        [ข้อมูลสรุปจากระบบ (Data Input)]
        {json.dumps(data_input, ensure_ascii=False, indent=2)}

        ---
        โครงสร้างรายงาน (ใช้ Markdown):

        # รายงานสรุปผลการดำเนินงาน: {kpi.event_name}

        ### ตารางสรุปประสิทธิภาพงาน (KPI Performance Dashboard)
        | ตัวชี้วัด (KPI) | ผลลัพธ์ | สถานะ | การตีความข้อมูล |
        | :--- | :--- | :--- | :--- |
        | อัตราการเช็กอิน (Check-in Rate) | {round(check_in_rate, 2)}% | | (เทียบกับเกณฑ์ 70%) |
        | ความพึงพอใจผู้เข้าชม (Visitor) | {kpi.visitor_score} | | (คะแนนเต็ม 5.0) |
        | ความพึงพอใจผู้แสดงงาน (Exhibitor) | {kpi.exhibitor_score} | | (คะแนนเต็ม 5.0) |
        | อัตราการทำแบบสอบถาม (Survey Rate) | {round(survey_rate, 2)}% | | (ความร่วมมือในการให้ข้อมูล) |

        ## 1. บทสรุปผู้บริหาร (Executive Summary)
        - วิเคราะห์ความสำเร็จเชิงปริมาณผ่านอัตราการเช็กอิน {round(check_in_rate, 2)}% เทียบกับเกณฑ์มาตรฐานอุตสาหกรรม (70%)
        - วิเคราะห์นัยสำคัญของกลุ่มเป้าหมายหลักคือ {max(kpi.occupations, key=kpi.occupations.get)} และผลกระทบต่อภาพรวมงาน

        ## 2. จุดแข็งและปัจจัยความสำเร็จ (Core Strengths)
        - สรุปสิ่งที่ทำได้ดีเยี่ยม (Top Good) โดยเชื่อมโยงคะแนน Rating กับคำชมใน Feedback (เช่น ระบบลงทะเบียนที่รวดเร็วช่วยสร้างความประทับใจแรกพบ)
        - ระบุแนวทางการรักษามาตรฐานนี้ไว้สำหรับงานในอนาคต

        ## 3. ประเด็นที่ต้องปรับปรุงเร่งด่วน (Critical Issues)
        - วิเคราะห์ช่องว่างความพึงพอใจระหว่าง Visitor และ Exhibitor (ถ้ามี)
        - สรุปประเด็นเชิงลบที่วิกฤตที่สุด ระบุจำนวนการกล่าวถึง (Mentions) และตัวอย่างปัญหาที่ส่งผลเสียต่อประสบการณ์ผู้ใช้
        - วิเคราะห์ช่องว่าง (Gap Analysis): คำนวณส่วนต่างระหว่างคะแนน Visitor และ Exhibitor หากต่างกันเกิน 0.5 ให้ระบุว่าเป็น "สภาวะขาดสมดุลเชิงกลยุทธ์ (Strategic Imbalance)"
        - ผลกระทบเชิงระบบ: อธิบายว่าปัญหาที่พบ กระทบต่อความคาดหวังเฉพาะด้านของแต่ละกลุ่มอย่างไร
        - การวิเคราะห์ความย้อนแย้ง: เช่น หากระบบลงทะเบียนดี (Visitor ชม) แต่ WiFi แย่ (Exhibitor บ่น) ให้ชี้ว่าเป็นปัญหาของการจัดสรรทรัพยากรที่ให้น้ำหนักกับ "ปริมาณผู้เข้าชม" มากกว่า "คุณภาพการปฏิบัติงาน"

        ## 4. ข้อเสนอแนะเชิงกลยุทธ์ (Future Action Plan)
        - เสนอแนวทางแก้ไขปัญหาเชิงเทคนิคและโลจิสติกส์แบบ 1-ต่อ-1 (Actionable Steps) เพื่อปิดช่องโหว่ที่พบในข้อ 3
        - กลยุทธ์การรักษาฐานผู้เข้าร่วมเดิม (Retention) และการขยายผลจากจุดแข็งเพื่อดึงดูดกลุ่มเป้าหมายใหม่
        - แนวทางแบบ Win-Win: เสนอทางออกที่ตอบโจทย์ Stakeholders ทุกฝ่ายพร้อมกัน (เช่น การปรับปรุง WiFi ไม่ใช่แค่เพื่อลดคำบ่น แต่เพื่อเพิ่มอัตราการตอบแบบสอบถาม (Survey Rate) และช่วยให้ Exhibitor ปิดการขายได้ดีขึ้น)
        - กลยุทธ์การรักษาความสัมพันธ์ (Retention Strategy): ระบุแผนการกู้คืนความเชื่อมั่นของกลุ่มที่ได้รับผลกระทบหากเกิดสภาวะขาดสมดุลเชิงกลยุทธ์ เพื่อป้องกันการสูญเสียผู้สนับสนุนหลักในอนาคต

        สไตล์การเขียน: เฉียบคม, ภาษาทางการสละสลวย, ข้อมูลแม่นยำ 100%, และสรุปจบทุกประเด็น"
        """

        async def stream_generator():
            yield (json.dumps({"check_in_rate": round(check_in_rate, 2), "survey_rate": round(survey_rate, 2)}, ensure_ascii=False) + "\n---\n").encode('utf-8')

            response = await client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[
                    {"role": "system", "content": "คุณคือที่ปรึกษาด้านอีเวนต์ที่วิเคราะห์สถิติได้อย่างแม่นยำและใช้ภาษาไทยระดับทางการที่ยอดเยี่ยม"},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                max_tokens=2000, # เผื่อไว้ให้เขียนรายงานจนจบ (ป้องกันประโยคค้าง)
                temperature=0.3  # ปรับให้ต่ำเพื่อให้ AI ทำตามกฎเหล็กได้แม่นยำขึ้น ไม่ฟุ้งซ่าน
            )

            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content.encode('utf-8')
                    await asyncio.sleep(0.01)

        return StreamingResponse(stream_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))