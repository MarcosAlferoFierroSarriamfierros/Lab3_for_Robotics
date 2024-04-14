%%
rosinit; %Conexi ́on con nodo maestro
%%
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); 
velMsg = rosmessage(velPub); %cramos de mensaje
%%
velMsg.Linear.X = 1; 
send(velPub,velMsg); %nviamos el mensaje
pause(1)
