module top (\a[0],\a[1],\a[2],\a[3],\b[0],\b[1],\b[2],\b[3],\c[0],\c[1],\c[2],\c[3]);
  input \a[0],\a[1],\a[2],\a[3],\b[0],\b[1],\b[2],\b[3];
  output \c[0],\c[1],\c[2],\c[3];
  wire n386,n387,n388,n389,n390,n391,n392,n393,n394,n395,n396,n397,n398,n399,n400,n401,n402,n403,n404,n405,n406,n407,n408,n409,n410 ;
  assign n386 = \a[0]  & ~\b[0] ;
  assign n387 = ~\a[0]  & \b[0] ;
  assign \c[0]  = n386 | n387;
  assign n389 = \a[0]  & \b[0] ;
  assign n390 = ~\a[1]  & ~\b[1] ;
  assign n391 = \a[1]  & \b[1] ;
  assign n392 = ~n390 & ~n391;
  assign n393 = n389 & ~n392;
  assign n394 = ~n389 & n392;
  assign \c[1]  = n393 | n394;
  assign n396 = n389 & ~n390;
  assign n397 = ~n391 & ~n396;
  assign n398 = ~\a[2]  & ~\b[2] ;
  assign n399 = \a[2]  & \b[2] ;
  assign n400 = ~n398 & ~n399;
  assign n401 = n397 & ~n400;
  assign n402 = ~n397 & n400;
  assign \c[2]  = ~n401 & ~n402;
  assign n404 = ~n397 & ~n398;
  assign n405 = ~n399 & ~n404;
  assign n406 = ~\a[3]  & ~\b[3] ;
  assign n407 = \a[3]  & \b[3] ;
  assign n408 = ~n406 & ~n407;
  assign n409 = n405 & ~n408;
  assign n410 = ~n405 & n408;
  assign \c[3]  = ~n409 & ~n410;
endmodule

