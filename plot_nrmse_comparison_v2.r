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
    x=read.delim(paste0('results/s',i,'.txt'),header=F)
    x=cbind(percent_missing=paste0(i,'%'),x)
    tbl=rbind(tbl,x)
}
colnames(tbl)[-1]=c('SVM','Lasso','Linear','RF','Factorization')
df=melt(tbl)
colnames(df)=c('percent_missing','Model','NRMSE')

#x=read.delim('avg.txt',header=F)
#df1=cbind(percent_missing=unique(tbl[,1]),x1=rep(0,4),x2=rep(6,4),y1=x,y2=x)
#colnames(df1)=c('percent_missing','x1','x2','y1','y2')

#tmp_col=c(p_jama[c(1:6)],"black")
#names(tmp_col)=c(colnames(tbl)[-1],"avg_imputation")
tmp_col=c(p_jama[c(2:6)])
names(tmp_col)=c(colnames(tbl)[-1])

p1 = ggplot(df,aes(x=Model,y=NRMSE)) +
    facet_wrap(~percent_missing,nrow=1) +
    theme_grey() +
    geom_violin(width=1,aes(fill=Model),colour="black",alpha=1,linetype=1,lwd=0.5,scale="width")+
    scale_fill_manual(values=tmp_col) +
    labs(x="Model",y="Spearman Correlation")+
    theme(axis.line.x = element_line(color="black", size = 0.5))+
    theme(axis.line.y = element_line(color="black", size = 0.5))+
    theme(axis.title.x = element_text(colour="black", size=20))+
    theme(axis.title.y = element_text(colour="black", size=20))+
    theme(axis.text.x = element_text(colour="black",angle = 45, hjust = 1, size=15))+
    theme(axis.text.y = element_text(colour="black",size=15))+
    theme(strip.background = element_blank())+
    theme(strip.text.x = element_text(colour="black", size=20))+
    theme(strip.text.y = element_text(colour="black", size=20))+
    theme(legend.position="none")
 #   geom_segment(aes(x = x1, y = y1, xend = x2, yend = y2), data = df1)
p1

# pdf(file="figures/percentage.pdf",width=12,height=5,useDingbats=F)
ggsave("figures/rank_correlation_5.png", width=12, height=5)
p1
dev.off()



