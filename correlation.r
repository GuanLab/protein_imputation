## name: plot_nrmse_comparison.r
## date: 06/18/2018

library(ggplot2)
library(reshape2)

# color
p_jama=c(
  'Limed Spruce' = '#374E55','Acapulco'     = '#79AF97',
  'Cerulean'     = '#00A1D5', 'Apple Blossom' = '#B24745',
  'Anzac'         = '#DF8F44', 'Kimberly'      = '#6A6599',
  'Makara'       = '#80796B')

tbl=NULL
for(i in c(5,8,10,20)){
    x=read.delim(paste0('ps',i,'.txt'),header=F)
    x=cbind(Percentage=paste0(i,'%'),x)
    tbl=rbind(tbl,x)
}
colnames(tbl)[-1]=c('Pearson','Rank')
df=melt(tbl)
colnames(df)=c('Percentage','Type','Correlation')

#x=read.delim('avg.txt',header=F)
#df1=cbind(percent_missing=unique(tbl[,1]),x1=rep(0,4),x2=rep(6,4),y1=x,y2=x)
#colnames(df1)=c('percent_missing','x1','x2','y1','y2')

#tmp_col=c(p_jama[c(1:6)],"black")
#names(tmp_col)=c(colnames(tbl)[-1],"avg_imputation")
tmp_col=c(p_jama[c(3:6)])
names(tmp_col)=c(colnames(tbl)[-1])

p1 = ggplot(df,aes(x=Percentage,y=Correlation,fill=Type)) +
    # facet_wrap(~percent_missing,nrow=1) +
    theme_grey() +
    geom_violin(width=0.6,colour="black",alpha=1,linetype=1,lwd=0.5,scale="width")+
    scale_fill_manual(values=tmp_col) +
    labs(x="Percentage",y="Correlation")+
    theme(axis.title.x = element_text(colour="black", size=20))+
    theme(axis.title.y = element_text(colour="black", size=20))+
    theme(axis.text.x = element_text(colour="black", size=15))+
    theme(axis.text.y = element_text(colour="black",size=15))+
    theme(strip.background = element_blank())+
    theme(strip.text.x = element_text(colour="black", size=20))+
    theme(strip.text.y = element_text(colour="black", size=20))+
    theme(legend.title = element_text(size=15))+
    theme(legend.text = element_text(size=15))
 #   geom_segment(aes(x = x1, y = y1, xend = x2, yend = y2), data = df1)
p1

ggsave("figures/correlation_lr.png", width=6, height=4)
p1
dev.off()



