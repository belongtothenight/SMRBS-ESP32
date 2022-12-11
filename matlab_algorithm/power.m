close all; clear all;

% read .mp3 file
[data, fs] = audioread('noise.mp3');

leftdata = copy(data);

% normalize data
data = data / abs(max(data));

alpha = 0.9999;
pln(1) = 0 ;
for i = 1 : length(data) - 1
    pln(i+1)=pln(i) * alpha + (data(i)^2) * (1 - alpha);
end

%% alpha=0.9998
alpha = 0.9998;
pln1(1) = 0 ;
for i = 1 : length(data) - 1
    pln1(i+1)=pln1(i) * alpha + (data(i)^2) * (1 - alpha);
end
%% alpha=0.9997
alpha = 0.9997;
pln2(1) = 0 ;
for i = 1 : length(data) - 1
    pln2(i+1)=pln2(i) * alpha + (data(i)^2) * (1 - alpha);
end
%% alpha=0.9996
alpha = 0.9996;
pln3(1) = 0 ;
for i = 1 : length(data) - 1
    pln3(i+1)=pln3(i) * alpha + (data(i)^2) * (1 - alpha);
end
%% alpha=0.9995
alpha = 0.9995;
pln4(1) = 0 ;
for i = 1 : length(data) - 1
    pln4(i+1)=pln4(i) * alpha + (data(i)^2) * (1 - alpha);
end
%% alpha=0.9994
alpha = 0.9994;
pln5(1) = 0 ;
for i = 1 : length(data) - 1
    pln5(i+1)=pln5(i) * alpha + (data(i)^2) * (1 - alpha);
end

%% plot
t = [ 0 : 1/fs : length(data)/fs]; % time in sec
t = t(1:end - 1);

%pf time
pft = [ 0 : c*(1/fs) : length(data)/fs];
pft = pft(1:end -1);


% subplot(2,1,1); plot(t,data); ylabel('audio');
% subplot(2,1,2); plot(pft,pf); ylabel('power');

plot(t,data,'k');
hold on; plot(t,pln1,'-r','LineWidth',1);
hold on; plot(t,pln2,'-g','LineWidth',1);
hold on; plot(t,pln3,'-b','LineWidth',1);
hold on; plot(t,pln4,'-m','LineWidth',1);
hold on; plot(t,pln5,'-y','LineWidth',1);

