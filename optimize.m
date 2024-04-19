function  f=optimize(x)
global I R data_num S;
[~,p]=ode45(@(t,p) SEIR(t,p,x), data_num, S); 
f=sum((I'- p(:,3)).^2 +(R'-p(:,4)).^2);
end