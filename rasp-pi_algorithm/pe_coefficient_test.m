function pe_coefficient_test(alpha)
clc;
t=0:0.01:100;
x=sin(2*pi*t);
p=x.^2;

%alpha=0.9;
pe = [0];
len=length(t);
for i=1:len
    pe = [pe alpha*pe(i) + (1-alpha)*p(i)];
    %fprintf('\n\nrun=%d', i);
    %fprintf('\nalpha=%f', alpha);
    %fprintf('\npe(i)=%f', pe(i));
    %fprintf('\np(i)=%f', p(i));
    %fprintf('\nalpha*pe(i)=%f', alpha*pe(i));
    %fprintf('\n(1-alpha)*p(i)=%f', (1-alpha)*p(i));
    %fprintf('\nans=%f\n', alpha*pe(i) + (1-alpha)*p(i));
    %pause;
end

maxpe = max(pe);
pebar = 0.7*maxpe;

fh = figure();
fh.WindowState = 'maximized';
hold on
plot(t,x);
plot(t,p);
plot(t,pe(2:end));
yline(pebar, 'linewidth', 3);
hold off
legend('signal', 'power', 'power estimation', '0.7*maxpe');
end

% T: cycle
% ex: if f=500Hz, alpha=0.999, pe stable at 1/500*12.3=0.0246s
% alpha=0.999, stable=12.3T(0.0246s)
% alpha=0.998, stable=6.24T(0.0125s)
% alpha=0.997, stable=4.22T(0.0084s)
% alpha=0.996, stalbe=3.23T(0.0065s)
