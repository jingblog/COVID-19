clear; 
close all; 
clc;

global I R S data_num;% 全局变量
SUM=329227746;  %某国家总人口数，此处选美国

% 拟合及预测选项设置
% 选择最近NUM天美国COVID-19疫情感染人数进行拟合，从昨天向前数NUM天
NUM=7;
%fmincon函数优化 分别表示SEIR模型中的beta, k, gamma, mu, E的初值
lb=[0.001 0.001 0.001 0.001 0.001];  %最小二乘拟合下限
ub=[1.0 1.0 1.0 1.0 1.0];   %最小二乘拟合上限
x0=[0.1 0.0101 0.011 0.012 0.011];  %最小二乘拟合初值
% 预测已有数据的MULTIPLY倍的天数，包括选择的NUM天
% 昨天前NUM天+昨天后(MULTIPLY-1)*NUM天
MULTIPLY=5;

% 图窗属性
fontsize=20;
linewidth=1;
fontname='宋体';

% 读入csv文件中数据数据
% 所需数据，通过python爬虫获取，get_data.py将网址改为对应国家的网址
[~, text] = xlsread("true data.csv","1:1");% 日期
total_cases=readmatrix("true data.csv",'Range','3:3'); %总确诊人数
total_deaths=readmatrix("true data.csv",'Range','4:4'); %总治愈
total_cures=readmatrix("true data.csv",'Range','5:5'); %总死亡
total_cases=total_cases(2:end);
total_cases(isnan(total_cases))=0;
total_deaths=total_deaths(2:end);
total_deaths(isnan(total_deaths))=0;
total_cures=total_cures(2:end);
total_cures(isnan(total_cures))=0;

active_cases=total_cases-total_cures-total_deaths;

% 日期格式转换
known_date_num=[1,length(text)]*nan;
known_date=strings(1,length(text));
for t=1:length(text)
    known_date(t)=cell2mat(text(t));
    known_date_num(t)=datenum(cell2mat(text(t)));
end

%清除附加数据
clear t text;

data_num=1:NUM; % 总数据数
I=active_cases((length(active_cases)-NUM+1):(length(active_cases)));  %感染者人数
R=total_cures((length(total_cures)-NUM+1):(length(total_cures)))+...
    total_deaths((length(total_deaths)-NUM+1):(length(total_deaths)));  %恢复者人数
known_date_num=known_date_num((length(known_date_num)-NUM+1):...
    (length(known_date_num)));
S = [SUM-100000 100000, I(1), R(1)];
%图窗1  Y轴为线性
f1=figure(1);
f1.WindowState='maximized';
hold on;

%真实数据
plot(known_date_num,I,'bo');
plot(known_date_num,R,'ko');

%拟合参数
[x,fval]=fmincon(@optimize,x0,[],[],[],[],lb,ub); % 最小二乘拟合

% 用拟合后的参数预测感染人数
% 预测数据量
predict_num=1:MULTIPLY*length(data_num);
% 设置为日期格式
predict_date=known_date_num(1):1:(known_date_num(1)+length(predict_num)-1); 
%求值
[~,p]=ode45(@(t,p)SEIR(t,p,x),predict_num,S); 
 
% 预测数据
plot(predict_date,round(p(:,1)),'r-');
plot(predict_date,round(p(:,2)),'g-');
plot(predict_date,round(p(:,3)),'b-');
plot(predict_date,round(p(:,4)),'k-');

%图窗属性
le=legend('感染者实际值I','恢复者实际值R', ...
    '易感者预测值S','潜伏者预测值E','感染者预测值I','恢复者预测值R', ...
    'Location','NorthEastOutside');
le.FontSize=fontsize;
startDate=known_date_num(1);
endDate=predict_date(MULTIPLY*NUM);
xData=linspace(startDate,endDate,7);
set(gca,'FontSize',fontsize);
set(gca,'XTick',xData,'XTickLabel',datestr(xData,'yy/mm/dd'));
axis tight;
box on;