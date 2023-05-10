install.packages("SPEI") 
install.packages("readr")
library(SPEI)
library(readr)
library(glue)

options(scipen=999)

df <- read_delim("C:/Users/User/Desktop/inmet_teste3.csv", 
                           ";", escape_double = FALSE, locale = locale(decimal_mark = ","), 
                           trim_ws = TRUE)





################################################################################
############################## SPI ############################################
################################################################################


#SPI6 <- spi(df$`PRECIPITACAO`,
#            scale = 6, na.rm = TRUE, dataopt = "monthly", cluster = TRUE, gamma.dist = TRUE, start = c(1992, 1), end = c(2022, 12))

SPI6 <- spi(ts(df$`PRECIPITACAO`, frequency = 12, start = c(1992, 1), end = c(2022, 12)), 
            scale = 6, na.rm = TRUE, dataopt = "monthly", start = c(1992, 1), end = c(2022, 12)) 
plot(SPI6)

?spi

#Teste de normalidade
SPI_shapiro <- shapiro.test(SPI6$fitted)$p.value

#Histograma
hist(SPI6$fitted, xlab = 'Frequência', ylab = 'Índice SPI', 
     main = 'Frequência índice SPI-6 (Brasília - 1992 a 2022)',
     col = 'cyan4', 
     breaks=c(-4, -2, -1.00, -0.5, 0.5, 1, 2, 4),
     labels = TRUE)
lines(density(SPI6$fitted, na.rm = TRUE))
polygon(density(SPI6$fitted, na.rm = TRUE),
        col=rgb(1,1,1,.2))
text(x = 0, y = 0.1, glue("Shapiro-Wilk p-valor: {round(SPI_shapiro, 4)}"),cex=1) 




################################################################################
############################## SPEI ############################################
################################################################################
#df <- df[df$TEMPERATURA_MAXIMA_MEDIA <= 32,]
df$PET <- hargreaves(Tmin = df$TEMPERATURA_MINIMA_MEDIA, 
                     Tmax = df$TEMPERATURA_MAXIMA_MEDIA, 
                     lat = -15.789722)
df$BAL <- df$PRECIPITACAO - df$PET

#SPEI3 <- spei(df$BAL,
#       scale = 3, na.rm = TRUE, dataopt = "monthly", cluster = TRUE, start = c(1992, 1), end = c(2022, 12))

SPEI3 <- spei(ts(df$BAL, frequency = 12, start = c(1992, 1), end = c(2022, 12)), 
        scale = 3, na.rm = FALSE, dataopt = "monthly", start = c(1992, 1), end = c(2022, 12)) 
plot(SPEI3)



#Teste de normalidade
SPEI_shapiro <- shapiro.test(SPEI3$fitted)$p.value

#Histograma
hist(SPEI3$fitted, xlab = 'Frequência', ylab = 'Índice SPEI', 
     main = 'Frequência índice SPEI-3 (Brasília - 1992 a 2022)',
     col = 'cyan4', breaks=c(-4, -2, -1.00, -0.5, 0.5, 1, 2, 4),
     labels=TRUE)
lines(density(SPEI3$fitted, na.rm = TRUE))
polygon(density(SPEI3$fitted, na.rm = TRUE),
        col=rgb(1,1,1,.2))
text(x = 0, y = 0.1, glue("Shapiro-Wilk p-valor: {round(SPEI_shapiro, 4)}"),cex=1) 


df$SPI6 <- SPI6$fitted
df$SPEI3 <- SPEI3$fitted
write.csv(df, "inmet_SPI_SPEI_indexes.csv", row.names=FALSE)

