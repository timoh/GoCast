% This is a ad-hoc plotting script due to the bugs in the javascript or the
% data representations.

% Also, in this file, two hundred previous data points used for the
% training is plotted, and thrirty newly predicted points are used as well.

%T = load('Training.txt');
%V = load('Validation.txt');
P = load('Prediction.txt');
A = load('Actual.txt');
%A = [zeros(1,4);A];

    %plot(sum(V'));
    %axis([1 200 -200 300])
    %figure;
    
    subplot(3,1,1)
    plot(sum(P'),'--rs','LineWidth',2,...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor','g',...
                'MarkerSize',10);
    axis([1 31 -600 700]) 
    hold on
    bar(sum(A(1:16,:)'),'c');
    legend('OverAll Prediction','Actual Expense')
    xlabel('Date','FontSize',12)
    ylabel('Balance','FontSize',12)
    
    
    
    subplot(3,1,2)
    hold off
    plot(P(:,1),'--rs','LineWidth',2,...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor','g',...
                'MarkerSize',10);
    axis([1 31 -100 100]) 
    hold on
    bar(A(1:16,1)','c')
    legend('OverAll Prediction','Actual Expense')
    xlabel('Date','FontSize',12)
    ylabel('Grocery Balance','FontSize',12)
    
    subplot(3,1,3)
    hold off
    plot(P(:,2),'--rs','LineWidth',2,...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor','g',...
                'MarkerSize',10);
    axis([1 31 -100 100])
    hold on
    bar(A(1:16,2)','c')
    legend('OverAll Prediction','Actual Expense')
    xlabel('Date','FontSize',12)
    ylabel('Entertain Balance','FontSize',12)
