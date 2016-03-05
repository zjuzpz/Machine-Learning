
data = importdata('u.data');
%Rrow = 943;
%Rcol = 1642;

R = zeros(942, 1642);
W = zeros(943, 1642);

for i=1:100000
    R(data(i,1),data(i,2)) = data(i,3);
    W(data(i,1),data(i,2)) = 1;
end

k = [10,50,100];
LSE = zeros(3,1);
finalResidual = zeros(3, 1);

option = struct();
option.dis = false;

% calculate LSE, which is the same as the result of finalResidual
for i=1:3
    [U,V,numIter,tElapsed,finalResidual(i)]=wnmfrule(R,k(i),W,option);
    LSE(i) = sqrt(sum(sum((W .* (R - U*V)).^2)));  
end


