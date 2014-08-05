begin
  if (.not. isvar("nyrStrt")) then      ; is nyrStrt on command line?
      nyrSrt = 1960
  end if

  if (.not. isvar("nyrLast")) then      ; is nyrLast on command line?
      nyrLast = 2002;
  end if

  print(nyrStrt)                        ; for illustrative purposes
  print(nyrLast)

end
