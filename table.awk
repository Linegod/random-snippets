awk -F, '
        NR == 1 {
                        gsub ( " ", X )
                        split ( $0, H, "," )
        }
        NR > 1 {
						printf "DATETIME "
                        for ( i = 1; i <= NF; i++ )
                                printf H[i] "=" $i " "
                        printf "\n"
        }
' OFS==
