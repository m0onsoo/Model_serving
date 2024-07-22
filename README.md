# Model_serving
Repository for serving models of the Palette service

## Description

Palette is a dating course recommendation platform for couples. <br>
This repository covers serving the [recommendation AI model](https://github.com/SJU-Capstone-DS-DayOne/Model) used in the Palette.

## Method

- Implement model serving by loading the FastAPI web framework on EC2
- Provides real-time recommendation inference results
- Access the database and parse the returned restaurant IDs by category

## Reference
* [FastAPI](https://fastapi.tiangolo.com/ko/) - A web framework for building APIs in Python
* [Amazon EC2](https://aws.amazon.com/ko/ec2/?gclid=Cj0KCQjwxqayBhDFARIsAANWRnRvCTl__zlVQEB4ILtf_H2FYSQWIVmPe2w-oz6mlGRcQ3mZbctN-gAaAnJvEALw_wcB&trk=bc3c5de1-7376-43c7-ad4f-f0f3f8248023&sc_channel=ps&ef_id=Cj0KCQjwxqayBhDFARIsAANWRnRvCTl__zlVQEB4ILtf_H2FYSQWIVmPe2w-oz6mlGRcQ3mZbctN-gAaAnJvEALw_wcB:G:s&s_kwcid=AL!4422!3!588924203019!e!!g!!ec2!16390049454!133992834459) - Server to load model API
