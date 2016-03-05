data = importdata('u.data');

R = zeros(942, 1642);
W = zeros(943, 1642);
R_predicted = zeros(942, 1642, 3);

option = struct();
option.dis = false;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      part 2   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% generate random number sequence from 1 to 100000
rand_index = randperm(100000);
k = [10,50,100];
errors = zeros(10, 10000,3);
mean_errors = zeros(10,3);

for cross_validation = 1:10
    % First initialize 9 training data and 1 testing data, with weight
    % ith 1/10 part will remain 0s,and the part before and after ith part
    % are inialized
    for i = 1:(cross_validation-1)*10000
            R(data(rand_index(i),1), data(rand_index(i),2)) = data(rand_index(i),3);
            W(data(rand_index(i),1), data(rand_index(i),2)) = 1;
    end
    
    for i = (cross_validation*10000 + 1):100000
            R(data(rand_index(i),1), data(rand_index(i),2)) = data(rand_index(i),3);
            W(data(rand_index(i),1), data(rand_index(i),2)) = 1;
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
    sprintf('For k = %d value', k(i));
    
    %Max error of 10 folds
    sprintf('Max error = %f', max(mean_errors(:, i)))
    
    %Min error of 10 folds
    sprintf('Min error = %f', min(mean_errors(:, i)))
    
    %Average error of 10 folds
    sprintf('Average error = %f', mean(mean_errors(:, i)))
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      end of part 2   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      part 3   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


threshold = linspace(0.1, 5.0, 50);
precisions = zeros(50,3); % row is the # of threshold values and col is the different values of k
recalls = zeros(50,3);
F_score = zeros(50,3);

for i = 1:50
for m=1:3
precisions(i,m)=length(find((R_predicted(:, :, m)>threshold(1,i)) & (R>3)))/length(find(R_predicted(:, :, m)>threshold(1,i)));
recalls(i, m)=length(find((R_predicted(:, :, m)>threshold(1,i)) & (R>3)))/length(find(R>3));
F_score(i,m) = 2*(precisions(i,m)*recalls(i,m)) / (precisions(i,m) + recalls(i,m));
end
end

%Plot precision over recall values
figure;
plot(recalls(:, 1), precisions(:, 1), 'b', recalls(:, 2), precisions(:, 2), 'r', recalls(:, 3), precisions(:, 3), 'g')
title('Precisions versus Recalls')
xlabel('Recalls')
ylabel('Precisions')
legend('k = 10', 'k = 50', 'k = 100')

% Plot precision over threshold values
figure;
plot(threshold(:), precisions(:, 1), 'b', threshold(:), precisions(:, 2), 'r', threshold(:), precisions(:, 3), 'g')
title('Precision versus Threshold')
xlabel('Threshold')
ylabel('Precisions')
legend('k = 10', 'k = 50', 'k = 100')

% Plot recall over threshold values
figure;
plot(threshold(:), recalls(:, 1), 'b', threshold(:), recalls(:, 2), 'r', threshold(:), recalls(:, 3), 'g')
title('Recalls versus Threshold')
xlabel('Threshold')
ylabel('Recalls')
legend('k = 10', 'k = 50', 'k = 100')

% Plot F_score over threshold values
figure;
plot(threshold(:), F_score(:, 1), 'b', threshold(:), F_score(:, 2), 'r', threshold(:), F_score(:, 3), 'g')
title('F_score versus Threshold')
xlabel('Threshold')
ylabel('F_score')
legend('k = 10', 'k = 50', 'k = 100')

% find the area under recalls-precisions curve
Area_under_ROC_curve = zeros(3,1);
for i = 1:3
Area_under_ROC_curve(i,:) = -trapz(recalls(:,i),precisions(:,i));
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      end of part 3   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        