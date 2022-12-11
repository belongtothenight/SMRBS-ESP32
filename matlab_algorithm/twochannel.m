close all; clear all;

% read .mp3 file (left)
[data, fs] = audioread('big.mp3');
leftdata = data(1:end,1);

% read .mp3 file (right)
[data, fs] = audioread('small.mp3');
rightdata = data(1:end,1);

% normalize data
rightdata = rightdata / abs(max(rightdata));
leftdata = leftdata / abs(max(leftdata));

%power estimation (left)
alpha = 0.9999;
pln(1) = 0 ;
for i = 1 : length(leftdata) - 1
    pln(i+1)=pln(i) * alpha + (leftdata(i)^2) * (1 - alpha);
end

%power estimation (right)
prn(1) = 0 ;
for i = 1 : length(rightdata) - 1
    prn(i+1)=prn(i) * alpha + (rightdata(i+1)^2) * (1 - alpha);
end

%plot
t = [ 0 : 1/fs : length(data)/fs]; % time in sec
t = t(1:end - 1);

%check which one is bigger
for i = 1 : length(data)
    if ( pln(i) > prn(i) )
        ch(i) = 2;
    elseif ( pln(i) < prn(i) )
        ch(i) = -2;
    else
        ch(i) = 0;
    end
end


plot(t,data,'k');
hold on; plot(t,pln,'-r','LineWidth',1);
hold on; plot(t,prn,'-g','LineWidth',1);
%hold on; plot(t,ch,'-y','lineWidth',2);

