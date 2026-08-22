conda activate py311
(base) newuser@ubuntu-pc:~/Code/AiFinancialAssistant$ conda activate py311
(py311) newuser@ubuntu-pc:~/Code/AiFinancialAssistant$ /home/newuser/miniconda3/envs/py311/bin/python /home/newuser/Code/AiFinancialAssistant/finance_r2ai/scripts/generate_dataset_gemini.py
INFO: Bắt đầu đọc dữ liệu từ: /home/newuser/Code/AiFinancialAssistant/instructions/data/ViFinQA_train.jsonl
INFO: 
--- Đang xử lý câu hỏi 1 ---
INFO: Q: Lãi tiền gửi năm 2018 của công ty mẹ CTCP Hàng không Vietjet (VJC) là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
WARNING: Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Hàng không Vietjet'], 'tickers': ['VJC'], 'years': ['2018'], 'report_type': 'separate', 'metric': 'Lãi tiền gửi', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 2 ---
INFO: Q: Số dư cho vay khách hàng ngành Thương mại của công ty mẹ Ngân hàng TMCP Á Châu (ACB) cuối năm 2022 là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['Ngân hàng TMCP Á Châu'], 'tickers': ['ACB'], 'years': ['2022'], 'report_type': 'separate', 'metric': 'số dư cho vay khách hàng ngành Thương mại', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 3 ---
INFO: Q: Chi phí dự phòng của Ngân hàng TMCP Sài Gòn Tài Lộc trong năm 2020 là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['Ngân hàng TMCP Sài Gòn Tài Lộc'], 'tickers': ['SGB'], 'years': ['2020'], 'report_type': 'consolidated', 'metric': 'Chi phí dự phòng', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 4 ---
INFO: Q: Lợi nhuận sau thuế của CTCP Chứng khoán FPT năm 2023 là bao nhiêu tỷ đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Chứng khoán FPT'], 'tickers': ['FTS'], 'years': ['2023'], 'report_type': 'consolidated', 'metric': 'lợi nhuận sau thuế', 'unit': 'tỷ đồng'}
WARNING: Không tìm thấy báo cáo nào cho FTS năm 2023
WARNING: Không tìm thấy bảng phù hợp!
INFO: 
--- Đang xử lý câu hỏi 5 ---
INFO: Q: Chi phí phạt của công ty mẹ SCR năm 2017 là bao nhiêu tỷ đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Địa ốc Sài Gòn Thương Tín'], 'tickers': ['SCR'], 'years': ['2017'], 'report_type': 'separate', 'metric': 'chi phí phạt', 'unit': 'tỷ đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 6 ---
INFO: Q: Lưu chuyển tiền thuần từ hoạt động kinh doanh của công ty mẹ VSC trong năm 2017 là bao nhiêu tỷ đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['Công ty cổ phần Container Việt Nam'], 'tickers': ['VSC'], 'years': ['2017'], 'report_type': 'separate', 'metric': 'Lưu chuyển tiền thuần từ hoạt động kinh doanh', 'unit': 'tỷ đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 7 ---
INFO: Q: Quỹ khen thưởng, phúc lợi của HT1 cuối năm 2019 là bao nhiêu tỷ đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Xi măng Vicem Hà Tiên'], 'tickers': ['HT1'], 'years': ['2019'], 'report_type': 'consolidated', 'metric': 'Quỹ khen thưởng, phúc lợi', 'unit': 'tỷ đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 8 ---
INFO: Q: Chi phí lương và các khoản khác theo lương của công ty mẹ CTCP Chứng khoán FPT trong năm 2021 là bao nhiêu tỷ đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Chứng khoán FPT'], 'tickers': ['FTS'], 'years': ['2021'], 'report_type': 'separate', 'metric': 'Chi phí lương và các khoản khác theo lương', 'unit': 'tỷ đồng'}
WARNING: Không tìm thấy báo cáo nào cho FTS năm 2021
WARNING: Không tìm thấy bảng phù hợp!
INFO: 
--- Đang xử lý câu hỏi 9 ---
INFO: Q: Chi phí khác của SAM năm 2023 là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP SAM Holdings'], 'tickers': ['SAM'], 'years': ['2023'], 'report_type': 'consolidated', 'metric': 'chi phí khác', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 10 ---
INFO: Q: Chi phí tài chính của công ty mẹ CTCP Phát triển Sunshine Homes năm 2021 là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Phát triển Sunshine Homes'], 'tickers': ['SSH'], 'years': ['2021'], 'report_type': 'separate', 'metric': 'chi phí tài chính', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 11 ---
INFO: Q: Số dư tiền gửi tại các TCTD khác cuối năm 2016 của Ngân hàng TMCP Đầu tư và Phát triển Việt Nam (BID) là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['Ngân hàng TMCP Đầu tư và Phát triển Việt Nam'], 'tickers': ['BID'], 'years': ['2016'], 'report_type': 'consolidated', 'metric': 'Số dư tiền gửi tại các TCTD khác', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 12 ---
INFO: Q: Vốn cổ phần đã phát hành của công ty mẹ VGT là bao nhiêu nghìn tỷ đồng vào cuối năm 2024?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['Tập đoàn Dệt May Việt Nam'], 'tickers': ['VGT'], 'years': ['2024'], 'report_type': 'separate', 'metric': 'vốn cổ phần đã phát hành', 'unit': 'nghìn tỷ đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 13 ---
INFO: Q: Tiền và các khoản tương đương tiền của công ty mẹ Tổng Công ty cổ phần Bia - Rượu - Nước giải khát Sài Gòn (SAB) vào cuối năm 2016 là bao nhiêu tỷ đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['Tổng Công ty cổ phần Bia - Rượu - Nước giải khát Sài Gòn'], 'tickers': ['SAB'], 'years': ['2016'], 'report_type': 'separate', 'metric': 'Tiền và các khoản tương đương tiền', 'unit': 'tỷ đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 14 ---
INFO: Q: Chi phí quản lý doanh nghiệp năm 2025 của công ty mẹ ASM là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Tập đoàn Sao Mai'], 'tickers': ['ASM'], 'years': ['2025'], 'report_type': 'separate', 'metric': 'chi phí quản lý doanh nghiệp', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 15 ---
INFO: Q: Thù lao của thành viên HĐQT Chu Thị Bình tại công ty mẹ MPC năm 2021 là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Tập đoàn Thủy sản Minh Phú'], 'tickers': ['MPC'], 'years': ['2021'], 'report_type': 'separate', 'metric': 'Thù lao của thành viên HĐQT Chu Thị Bình', 'unit': 'triệu đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 16 ---
INFO: Q: Số dư vay ngắn hạn của công ty mẹ CEO cuối năm 2025 là bao nhiêu tỷ đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 200 OK"
INFO: Parsed: {'company_names': ['CTCP Tập đoàn C.I.O'], 'tickers': ['CEO'], 'years': ['2025'], 'report_type': 'separate', 'metric': 'vay ngắn hạn', 'unit': 'tỷ đồng'}
WARNING: Không lấy được nội dung bảng dạng Markdown!
INFO: 
--- Đang xử lý câu hỏi 17 ---
INFO: Q: Lãi thuần từ hoạt động dịch vụ của Ngân hàng TMCP Sài Gòn - Hà Nội (SHB) năm 2018 là bao nhiêu triệu đồng?
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent "HTTP/1.1 429 Too Many Requests"
WARNING: Lỗi gọi Gemini API (lần 1/3): 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 15, model: gemini-3.5-flash-lite\nPlease retry in 16.366667189s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-3.5-flash-lite'}, 'quotaValue': '15'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '16s'}]}}
INFO: Phát hiện lỗi 429 Quota Exceeded. Tạm dừng 60 giây trước khi thử lại...
^CTraceback (most recent call last):
  File "/home/newuser/Code/AiFinancialAssistant/finance_r2ai/src/services/gemini_client.py", line 43, in generate_content
    response = self.client.models.generate_content(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/google/genai/models.py", line 6550, in generate_content
    response = self._generate_content(
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/google/genai/models.py", line 4978, in _generate_content
    response = self._api_client.request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/google/genai/_api_client.py", line 1747, in request
    response = self._request(http_request, http_options, stream=False)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/google/genai/_api_client.py", line 1534, in _request
    return self._retry(self._request_once, http_request, stream)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/tenacity/__init__.py", line 470, in __call__
    do = self.iter(retry_state=retry_state)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/tenacity/__init__.py", line 371, in iter
    result = action(retry_state)
             ^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/tenacity/__init__.py", line 413, in exc_check
    raise retry_exc.reraise()
          ^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/tenacity/__init__.py", line 184, in reraise
    raise self.last_attempt.result()
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/concurrent/futures/_base.py", line 449, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/concurrent/futures/_base.py", line 401, in __get_result
    raise self._exception
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/tenacity/__init__.py", line 473, in __call__
    result = fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/google/genai/_api_client.py", line 1511, in _request_once
    errors.APIError.raise_for_response(response)
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/google/genai/errors.py", line 173, in raise_for_response
    cls.raise_error(response.status_code, response_json, response)
  File "/home/newuser/miniconda3/envs/py311/lib/python3.11/site-packages/google/genai/errors.py", line 202, in raise_error
    raise ClientError(status_code, response_json, response)
google.genai.errors.ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 15, model: gemini-3.5-flash-lite\nPlease retry in 16.366667189s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-3.5-flash-lite'}, 'quotaValue': '15'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '16s'}]}}

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/newuser/Code/AiFinancialAssistant/finance_r2ai/scripts/generate_dataset_gemini.py", line 284, in <module>
    main()
  File "/home/newuser/Code/AiFinancialAssistant/finance_r2ai/scripts/generate_dataset_gemini.py", line 227, in main
    parsed_query = parse_query(client, question)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/Code/AiFinancialAssistant/finance_r2ai/scripts/generate_dataset_gemini.py", line 127, in parse_query
    response_text = client.generate_content(
                    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/newuser/Code/AiFinancialAssistant/finance_r2ai/src/services/gemini_client.py", line 55, in generate_content
    time.sleep(60)
KeyboardInterrupt

(py311) newuser@ubuntu-pc:~/Code/AiFinancialAssistant$ ^C
(py311) newuser@ubuntu-pc:~/Code/AiFinancialAssistant$ 