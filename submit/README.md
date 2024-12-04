# Fantasy Football Agent: Find Optimal Draft Picks using Genetic Algorithms

----
Overview
---
This project provides an AI agent that uses a genetic algorithm to calculate the optimal draft picks
for the year.


{\rtf1\ansi\ansicpg936\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica-Bold;\f1\fswiss\fcharset0 Helvetica;\f2\fswiss\fcharset0 Helvetica-Oblique;
}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\qc\partightenfactor0

\f0\b\fs24 \cf0 Guideline for the genetic algo code\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 Please READ it carefully and you can make the algo run as you wish.\
\
\
Quick Start:\
\

\f1\b0 \ul Step1 Get the data\ulnone \
run 
\f2\i datainjectionFromAWS.py
\f1\i0  to get the cooked data from AWS database\
\
\ul Step2 Save the data to your path\ulnone \
find a path to store the source data, copy the path of it into your computer\
\
\
\ul Step3 Run the driver\ulnone \
run runWithADP.py , it\'92s the main driver\
\
\
\ul Step4 Check output\ulnone \
\pard\pardeftab720\partightenfactor0
\cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 1 - a chart(comparison final team with adp team) \
2- an excel( final picked team with its data by years) \
3- an excel(recommend agent with its weights) \
4- an excel( adp reference team with its data by years)\kerning1\expnd0\expndtw0 \outl0\strokewidth0 \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\b \cf0 \
}