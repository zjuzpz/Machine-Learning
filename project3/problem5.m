%{
u.data  -- The full u data set, 100000 ratings by 943 users 
on 1682 items.
Each user has rated at least 20 movies.  Users and items are
numbered consecutively from 1.  The data is randomly
ordered. This is a tab separated list of 
user id | item id | rating | timestamp. 
%}

data = importdata('u.data');
R = zeros(942, 1642);
W = zeros(943, 1642);
option = struct();
option.dis = false;
option.lambda = 0.01;
rand_index = randperm(100000);
R_predicted = zeros(942, 1642, 3);

for cross_validation = 1:10
    % First initialize 9 training data and 1 testing data, with weight
    %R_tmp = R;
    for i = 1:(cross_validation-1)*10000
       W(data(rand_index(i),1), data(rand_index(i),2)) = data(rand_index(i),3);
       R(data(rand_index(i),1), data(rand_index(i),2)) = 1;
    end

    %ith block will be full of zeros
    for i=(cross_validation*10000 + 1):100000
      W(data(rand_index(i),1), data(rand_index(i),2)) = data(rand_index(i),3);
      R(data(rand_index(i),1), data(rand_index(i),2)) = 1;
    end

    for idx=1:3
      [U,V,numIter,tElapsed,finalResidual]=wnmfrule(R,k(idx),W,option);
      UV = U*V;
      sum_errors = 0;

      % calculate errors in testing data
      for i=((cross_validation-1)*10000 + 1):cross_validation*10000
        % Compute absolute error and add it to sum
        row = data(rand_index(i),1);
        col = data(rand_index(i),2);
        R_predicted(row, col, idx) = UV(row, col);
       end
    end
end



%Write predicted data and actual data in file, adn use python to deal with
%the data
p1 = mfilename('fullpath');
i=findstr(p1,'\');
p1=p1(1:i(end));
p = cd(p1);

path = [p, '\', 'problem5data\', 'actualData.txt'];
fid = fopen(path, 'wt');
for row = 1:942
    for col = 1:1642
        fprintf(fid, '%d ', W(row, col));
    end
    fprintf(fid, '\n');
end
fclose(fid);


for i = 1:3
    path = [p, '\', 'problem5data\', 'predictedR', num2str(i), '.txt'];
    fid = fopen(path, 'wt'); 
    for row = 1:942
        for col = 1:1642
            fprintf(fid, '%d ', R_predicted(row, col, i)); 
        end
        fprintf(fid, '\n');
    end
    fclose(fid);
end