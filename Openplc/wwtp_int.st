
PROGRAM My_Program
  VAR

    Oxygen AT %IW0 : INT := 10;
    Nitrate AT %IW1 : INT := 5;
    Ammonium AT %IW2 : INT := 2;
    Temperature AT %IW3 : INT := 8 ;   
    InternalRecirculationPump AT %QW0 : INT := 25000;
    WasteSludgePump AT %QW1 : INT := 106;
    AirPump AT %QW2 : INT := 100;
  END_VAR
  VAR
    MOVE5_OUT : INT;
  END_VAR
    MOVE5_OUT := MOVE(Temperature);

END_PROGRAM

CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : My_Program;
  END_RESOURCE
END_CONFIGURATION
