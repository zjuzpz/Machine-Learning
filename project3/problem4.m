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

for i=1:100000
    W(data(i,1),data(i,2)) = data(i,3);
    R(data(i,1),data(i,2)) = 1;
end

%W(find(R > 0)) = 1;

k = [10,50,100];
LSE = zeros(3,1);
finalResidual = zeros(3, 1);

option = struct();
option.dis = false;

% calculate LSE, which is the same as the result of finalResidual
for j = [0, 0.01, 0.1, 1]
    option.lambda = j;
    for i=1:3
        s=sprintf('Result of k = %0.0d and lambda = %0.2d', k(i), j);
        disp(s)
    %    disp(['result of k = %0.0d and lambda = %0.2d', k(i), j]);
        [U,V,numIter,tElapsed,finalResidual(i)]=wnmfrule(R,k(i),W,option);
        LSE(i) = sqrt(sum(sum((W .* (R - U*V)).^2)));  
    end
end

rand_index = randperm(100000);
%steps = [1,10001,20001,30001,40001,50001,60001,70001,80001,90001];

errors = zeros(10, 10000,3);
mean_errors = zeros(10,3);


for lambda = [0.01, 0.1, 1]
    sprintf('For lambda = %0.2d', lambda)
    option.lambda = lambda;
    R_predicted = zeros(942, 1642, 3);
    R = zeros(942, 1642);
    W = zeros(943, 1642);

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
            sum_errors = sum_errors + abs(UV(row, col) - R(row, col));
            R_predicted(row, col, idx) = UV(row, col);
           end
           mean_errors(cross_validation, idx) = sum_errors / 10000;
        end
    end

    for i=1:3
        sprintf('For k = %0.0d', k(i))

        %Max error of 10 folds
        sprintf('Max error = %f', max(mean_errors(:, i)))

        %Min error of 10 folds
        sprintf('Min error = %f', min(mean_errors(:, i)))

        %Average error of 10 folds
        sprintf('Average error = %f', mean(mean_errors(:, i)))
    end
   
    threshold = linspace(0, 1.2, 50);
    precisions = zeros(50,3); % row is the # of threshold values and col is the different values of k
    recalls = zeros(50,3);
    F_score = zeros(50,3);
    hit = 0;
    total =0;
    right = 0;
    for i = 1:50
        for m=1:3
            for row = 1 : 942
                for col = 1:1682
                    if R_predicted(row, col, m) > threshold(i) && W(row, col) > 3
                        hit = hit + 1;
                    end
                    if R_predicted(row, col, m) > threshold(i) && W(row, col) > 0
                        total = total + 1;
                    end
                    if W(row, col) > 3
                        right = right + 1;
                    end
                end
            end
            precisions(i,m)= hit / total;
            recalls(i, m)=hit / right;
        end
    end

    %Plot precision over recall values
    figure;
    plot(recalls(:, 1), precisions(:, 1), 'b', recalls(:, 2), precisions(:, 2), 'r', recalls(:, 3), precisions(:, 3), 'g')
    title('Precisions versus Recalls')
    xlabel('Recalls')
    ylabel('Precisions')
    legend('k = 10', 'k = 50', 'k = 100')

    figure;
    plot(threshold(:), precisions(:, 1), 'b', threshold(:), precisions(:, 2), 'r', threshold(:), precisions(:, 3), 'g')
    title('Precision versus Threshold')
    xlabel('Threshold')
    ylabel('Precisions')
    legend('k = 10', 'k = 50', 'k = 100')


end

